import subprocess
import time
import random
import os
import argparse

def terminate(process: subprocess.Popen):
    if process:
        print("Terminating process...")
        process.terminate()
        process.wait()


def run_program(args: list) -> subprocess.Popen:
    return subprocess.Popen(
        args, 
        preexec_fn=os.setpgrp
    )


def run(interval, chance, wait_time, args):
    process = None
    try:
        print("Starting process...")
        process = run_program(args)
        time.sleep(wait_time)
        while True:
            if process.poll() is not None:
                print("Process terminated.")
                break
            if random.random() < chance:
                terminate(process)
                print("Restarting process...")
                process = run_program(args)
                time.sleep(wait_time)
            else:
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\nForcing end...")
        terminate(process)


def main():
    parser = argparse.ArgumentParser(description="Auto-restart a program")
    parser.add_argument("-i", "--interval", type=int, help="Interval in seconds", default=1)
    parser.add_argument("-c", "--chance",type=float, help="Chance of restart", default=0.01)
    parser.add_argument("-s", "--seed", type=int, help="Seed for random number generator", default=42)
    parser.add_argument("-w", "--wait", type=int, help="Wait time before running the loop", default=3)
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Program arguments")
    args = parser.parse_args()
    if len(args.args) < 1:
        parser.error("Please provide a program to run.")
        exit(1)
    if args.interval == 0:
        print("Starting program without auto-restart...")
        subprocess.run(args.args)
        print("Program finished.")
        exit(0)
    random.seed(args.seed)
    run(args.interval, args.chance, args.wait, args.args)


if __name__ == "__main__":
    main()
