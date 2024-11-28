import re 
import subprocess 
def get_gpu_usage():
    try:
        # Run the `nvidia-smi` command and capture the output
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Regular expressions to extract memory usage and GPU utilization
        memory_pattern = re.compile(r"(\d+)MiB / (\d+)MiB")
        utilization_pattern = re.compile(r"(\d+)%")

        gpus = []
        memory_matches = memory_pattern.findall(output)
        utilization_matches = utilization_pattern.findall(output)

        for idx, (used, total) in enumerate(memory_matches):
            gpu_info = {
                "GPU": idx,
                "Memory_Used_MiB": int(used),
                "Memory_Total_MiB": int(total),
                "Memory_Usage_Percentage": round((int(used) / int(total)) * 100, 2)
            }
            if idx < len(utilization_matches):
                gpu_info["GPU_Utilization_Percentage"] = int(utilization_matches[idx])
            else:
                gpu_info["GPU_Utilization_Percentage"] = None

            gpus.append(gpu_info)

        return gpus

    except Exception as e:
        print(f"Error while retrieving GPU usage: {e}")
        return []