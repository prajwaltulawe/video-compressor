import argparse
from compressor.queue_manager import QueueManager
from compressor.utils import ensure_dir

def main():

    parser = argparse.ArgumentParser(
        description="Video Compressor"
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input video files"
    )

    parser.add_argument(
        "--output-dir",
        default="output"
    )

    parser.add_argument(
        "--codec",
        default="h264",
        choices=["h264", "hevc", "vp9", "av1"]
    )

    parser.add_argument(
        "--container",
        default="mp4",
        choices=["mp4", "mkv", "avi", "mov", "webm"]
    )

    parser.add_argument(
        "--resolution",
        default=None,
        help="1280:720"
    )

    parser.add_argument(
        "--bitrate",
        default=None,
        help="4M"
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=None
    )

    parser.add_argument(
        "--preset",
        default="balanced",
        choices=["fast", "balanced", "high"]
    )

    parser.add_argument(
        "--disable-hw",
        action="store_true"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=2
    )

    args = parser.parse_args()

    ensure_dir(args.output_dir)

    queue = QueueManager(
        workers=args.workers
    )

    for file in args.inputs:

        queue.add_job({
            "input_file": file,
            "output_dir": args.output_dir,
            "codec": args.codec,
            "container": args.container,
            "resolution": args.resolution,
            "bitrate": args.bitrate,
            "fps": args.fps,
            "preset": args.preset,
            "hw_accel": not args.disable_hw
        })

    queue.process()

if __name__ == "__main__":
    main()