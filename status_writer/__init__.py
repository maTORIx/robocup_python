from status_writer import init_writer, log_writer, hear_writer

status_writer_list = [
    init_writer.write_initial_status,
    log_writer.write_log,
    hear_writer.write_heared_status
]