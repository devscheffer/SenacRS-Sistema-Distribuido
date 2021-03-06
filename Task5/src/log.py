import datetime


def fn_write_log(
    event_type: str,
    event_data: dict,
    file_name : str = "geral",
    log_path  : str = "./Task5/log"
    ) -> None:
    path_output = f"{log_path}/log_{file_name}.txt"
    log_text = {"event_type": event_type, "event_data": event_data}
    with open(path_output, "a") as file:
        current_time = datetime.datetime.now()
        file.write(f"{current_time},{log_text}\n")
