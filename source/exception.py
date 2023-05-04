import sys


def error_message_details(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    message=f"error has occured in python program name [{file_name}] at the line [{exc_tb.tb_lineno}] and the error message is [{str(error)}]"
    return message


class customException(Exception):
    def __init__(self,message,error_detail:sys):
        super().__init__(message)
        self.message=error_message_details(message,error_detail=error_detail)
    
    def  __str__(self):
        return self.message


