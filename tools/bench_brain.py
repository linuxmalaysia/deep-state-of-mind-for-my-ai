"""
DSOM Spatial Brain Benchmark Tool.

Measures read latency and byte throughput across .agents/brain and .agents/skills
files to calibrate token and context performance multipliers for native OS and simulated
mobile (Android Termux) environments.
"""
import os
import time
import sys

def get_files(directories, extension=".md"):
    """
    Recursively discover all files with a given extension across target directories.

    Parameters:
        directories (list[str]): Directory paths to scan.
        extension (str): File extension filter (defaults to '.md').

    Returns:
        list[str]: Absolute or relative file paths matching the extension.
    """
    files = []
    for d in directories:
        if not os.path.exists(d):
            continue
        for root, _, filenames in os.walk(d):
            for filename in filenames:
                if filename.endswith(extension):
                    files.append(os.path.join(root, filename))
    return files

def bench_read(files):
    """
    Measure aggregate byte read volume and wall-clock execution time.

    Parameters:
        files (list[str]): List of file paths to read.

    Returns:
        tuple[int, float]: Total bytes read and elapsed time in seconds.
    """
    start = time.perf_counter()
    total_bytes = 0
    for f in files:
        with open(f, 'rb') as fp:
            data = fp.read()
            total_bytes += len(data)
    end = time.perf_counter()
    return total_bytes, end - start

if __name__ == "__main__":
    target_dirs = [".agents/brain", ".agents/skills"]
    files = get_files(target_dirs)
    if not files:
        print("No files found to benchmark.")
        sys.exit(1)
    
    total_bytes, elapsed = bench_read(files)
    
    print(f"Benchmarked {len(files)} files ({total_bytes} bytes).")
    print(f"Total read time (Native OS baseline): {elapsed*1000:.2f} ms")
    print(f"Average read time per file: {(elapsed*1000)/len(files):.2f} ms")
    
    # Simulate Android FUSE latency
    fuse_multiplier = 3.5  # Estimated 2-5x multiplier for Samsung Note 10
    print("\n--- Android Termux (Samsung Note 10) Simulated Extrapolation ---")
    print(f"Estimated FUSE multiplier: {fuse_multiplier}x")
    print(f"Simulated total read time: {(elapsed*1000)*fuse_multiplier:.2f} ms")
    print(f"Simulated average read time per file: {((elapsed*1000)/len(files))*fuse_multiplier:.2f} ms")
