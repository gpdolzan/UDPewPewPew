import datetime

class Logger:
    def __init__(self, log_type: str):
        if log_type not in ['client', 'server']:
            raise ValueError("log_type must be either 'client' or 'server'")
        
        self.log_type = log_type
        self.filename = self.generate_filename()
        self.write_header_to_file()

    def write_header_to_file(self):
        header = [
            "=====================================================================================",
            f"Inicio da execucao: programa que implementa o {self.log_type} de streaming de video com udp.",
            "Gabriel Pimentel Dolzan e Tulio de Padua Dutra - Disciplina Redes de Computadores II",
            "====================================================================================="
        ]
        
        with open(self.filename, 'w') as f:
            for line in header:
                f.write(line + "\n")

    def generate_filename(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"logs/{self.log_type}_{timestamp}.log"

    def log(self, message, level="INFO"):
        with open(self.filename, 'a') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] [{level}] {message}\n")

    def info(self, message):
        self.log(message, "INFO")

    def warning(self, message):
        self.log(message, "WARNING")

    def error(self, message):
        self.log(message, "ERROR")

    def debug(self, message):
        self.log(message, "DEBUG")

# Example of how to use the Logger class:

if __name__ == "__main__":
    server_logger = Logger("server")
    server_logger.info("Server started.")

    client_logger = Logger("client")
    client_logger.info("Client started.")
