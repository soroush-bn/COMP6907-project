import re 
import subprocess 
import torch 
def get_gpu_usage():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        memory_pattern = re.compile(r"(\d+)MiB /  (\d+)MiB")
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
                gpu_info["GPU_Fan_Percentage"] = int(utilization_matches[0])
                gpu_info["GPU_Utilization_Percentage"] = int(utilization_matches[1])
            else:
                gpu_info["GPU_Fan_Percentage"] = None
                gpu_info["GPU_Utilization_Percentage"] = None

            gpus.append(gpu_info)

        return gpus

    except Exception as e:
        print(f"Error while retrieving GPU usage: {e}")
        return []
    

def free_gpu(model):
    del model
    torch.cuda.empty_cache()
    import gc
    gc.collect()

def get_gpu_details_string(gpu_details):
    text = ""
    for i, gpu in enumerate(gpu_details):
        text += f"### GPU {i} Details \n\n"
        text += f"**Used Memory (MiB):** {gpu['Memory_Used_MiB']}\n\n"
        text += f"**Total Memory (MiB):** {gpu['Memory_Total_MiB']}\n\n"
        text += f"**Memory Usage (%):** {gpu['Memory_Usage_Percentage']}\n\n"
        text += f"**Fan Usage (%):** {gpu['GPU_Fan_Percentage']}\n\n"
        text += f"**Utilization (%):** {gpu['GPU_Utilization_Percentage']}\n\n"
    return text
