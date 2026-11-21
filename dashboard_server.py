import threading
import rclpy
from flask import Flask, jsonify, render_template_string

from unicycle_subscriber import UnicycleSubscriber


app = Flask(__name__)
robot = None

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unicycle Robot Simulator</title>
    <style>
        body {
            background: #101827;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }

        canvas {
            background: #ffffff;
            border-radius: 12px;
            margin-top: 20px;
        }

        .stats {
            margin: 15px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>Unicycle Robot Simulator</h1>

    <div class="stats" id="stats">Waiting for robot...</div>

    <canvas id="map" width="700" height="550"></canvas>

    <script>
        const canvas = document.getElementById("map");
        const ctx = canvas.getContext("2d");
        const stats = document.getElementById("stats");

        const scale = 65;
        const path = [];

        function drawGrid() {
            ctx.strokeStyle = "#e5e7eb";
            ctx.lineWidth = 1;

            for (let x = 0; x <= canvas.width; x += scale) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }

            for (let y = 0; y <= canvas.height; y += scale) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
        }

        function drawRobot(x, y, theta) {
            const px = canvas.width / 2 + x * scale;
            const py = canvas.height / 2 - y * scale;

            ctx.save();
            ctx.translate(px, py);
            ctx.rotate(-theta);

            ctx.fillStyle = "#ef4444";
            ctx.beginPath();
            ctx.moveTo(20, 0);
            ctx.lineTo(-12, -11);
            ctx.lineTo(-12, 11);
            ctx.closePath();
            ctx.fill();

            ctx.restore();
        }

        function render(data) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            drawGrid();

            const px = canvas.width / 2 + data.x * scale;
            const py = canvas.height / 2 - data.y * scale;

            path.push([px, py]);

            ctx.strokeStyle = "#2563eb";
            ctx.lineWidth = 3;
            ctx.beginPath();

            path.forEach((point, index) => {
                if (index === 0) {
                    ctx.moveTo(point[0], point[1]);
                } else {
                    ctx.lineTo(point[0], point[1]);
                }
            });

            ctx.stroke();

            drawRobot(data.x, data.y, data.theta);

            stats.textContent =
                `X: ${data.x.toFixed(2)} m | ` +
                `Y: ${data.y.toFixed(2)} m | ` +
                `Theta: ${data.theta.toFixed(2)} rad | ` +
                `V: ${data.v.toFixed(2)} m/s | ` +
                `Omega: ${data.omega.toFixed(2)} rad/s`;
        }

        async function update() {
            try {
                const response = await fetch("/api/pose");
                const data = await response.json();
                render(data);
            } catch (error) {
                console.error("Failed to fetch robot pose:", error);
            }
        }

        setInterval(update, 100);
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/pose")
def get_pose():
    return jsonify({
        "x": robot.x,
        "y": robot.y,
        "theta": robot.theta,
        "v": robot.v,
        "omega": robot.omega
    })


def run_ros():
    try:
        rclpy.spin(robot)
    except KeyboardInterrupt:
        pass


def main():
    global robot

    rclpy.init()
    robot = UnicycleSubscriber()

    ros_thread = threading.Thread(
        target=run_ros,
        daemon=True
    )
    ros_thread.start()

    try:
        app.run(
            host="0.0.0.0",
            port=5050,
            debug=False,
            use_reloader=False
        )
    finally:
        robot.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

        ros_thread.join(timeout=2.0)


if __name__ == "__main__":
    main()
