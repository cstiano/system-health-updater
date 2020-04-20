# System Health Updater

System Health Updater is a tool that gets a list of health informations of the machine that it is running the script. This informations are uptaded through a POST request to a consumer, receiving a json object with theses data.

The json object with all the health data follow this format bellow:

```
{
    'cpu_count': NUMBER, 
    'cpu_load': NUMBER, 
    'cpu_percent': NUMBER, 
    'ram': 
    {
        'total_ram': NUMBER, 
        'used_ram': NUMBER, 
        'memory_used_percent': NUMBER
    }, 
    'disk': 
    {
        'total_disk_space': NUMBER, 
        'used_disk_space': NUMBER, 
        'free_disk_space': NUMBER, 
        'read_write': 
        {
            'read': STRING, 
            'written': STRING
        }
    }
}
```

### Configuration

Before run the Dockerfile, change the the BASE_URL and ROUTE at the Dockerfile, with the base url and route that you want to send the POST request of the System Health Updater.

```
CMD [ "python", "./main.py <BASE_URL> <ROUTE>"]
```