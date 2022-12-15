from ..parser.position import Span

class LogRecord:
    """ A record of a log. """
    
    message: str
    """ The record's message. """
    
    span: Span
    """ The record's span. """
    
    def __init__(self, message: str, span: Span) -> None:
        """ Initialize the record's message and span. """
        
        self.message = message
        self.span = span
    
    
    def __str__(self) -> str:
        """ Return the record's string. """
        
        if self.span.start.offset < 0:
            return self.message
        
        return f"{self.span}: {self.message}"


class Log:
    """ A sorted log of records. """
    
    records: list[LogRecord]
    """ The log's records. """
    
    def __init__(self) -> None:
        """ Initialize the log's records. """
        
        self.clear()
    
    
    def has_records(self) -> bool:
        """ Return whether the log has any records. """
        
        return len(self.records) > 0
    
    
    def clear(self) -> None:
        """ Clear the log's records. """
        
        self.records = []
    
    
    def log(self, message: str, span: Span = None) -> None:
        """ Insert a new record into the log. """
        
        if span is None:
            span = Span()
            span.start.offset = -1
        
        record: LogRecord = LogRecord(message, span)
        index: int = len(self.records)
        
        while index > 0:
            previous: LogRecord = self.records[index - 1]
            
            if record.span.start.offset >= previous.span.start.offset:
                break
            
            index -= 1
        
        self.records.insert(index, record)
    
    
    def print_records(self) -> None:
        """ Print the log's records. """
        
        print("--------- Error Log ---------")
        
        for record in self.records:
            print(record)
        
        print("-----------------------------")
