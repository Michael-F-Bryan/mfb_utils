import re


class StringScanner:
    """
    A scanner very similar to Ruby's StringScanner. 
    
    It is mainly designed to make lexing easy, but I'm sure there are loads 
    of other useful applications too.  
    """
    def __init__(self, text=None, position=0):
        self.text = text
        self.pos = position
        self.match = None
        
    def search(self, pattern, advance_pointer=True, 
                return_string=True, from_pointer=True):
        """
        The function that does most of the heavy lifting. The 
        """
        search_func = re.match if from_pointer else re.search
        pattern = re.compile(pattern)
        
        match = search_func(pattern, self.text[self.pos:])
        
        # Set the match register using whatever we found
        if match:
            index = match.span()[0] + len(match.group())
            self.match = self.text[self.pos:self.pos + index]
        else:
            self.match = None
            
        # Advance the pointer if necessary
        if advance_pointer:
            self.pos += len(self.match) if self.match else 0
            
        # And finally return something. Either the match itself
        # or the number of characters found
        if return_string:
            return self.match
        else:
            return len(self.match) if self.match else 0
        
    def check(self, pattern):
        """
        This will check the string for a pattern, returning the matched 
        string or None if it wasn't found.  
        
        `check()` doesn't advance the scan pointer, but the match register is 
        still affected.  
        """
        return self.search(pattern, advance_pointer=False)
    
    def scan(self, pattern):
        """
        Checks for a match, using the same arguments as `check()`.  If a 
        match is found, increment the scanner pointer accordingly and return 
        the matched string.  
        
        Failed matches return None instead of raising an error.
        """
        return self.search(pattern)
    
    def skip(self, pattern):
        """
        Skip the specified pattern, returning the number of characters 
        skipped and setting the match register.  
        """
        return self.search(pattern, return_string=False)
    
    def unscan(self):
        """
        Using whatever is in the match register, revert to the previous 
        scanner state.  
        
        Note
        ----
        You can only go back one step.
        """
        self.pos -= len(self.match) if self.match else 0
        self.match = None
        
    def getch(self):
        """
        Get the next character from the string.
        """
        character = self.current_char
        self.pos += 1
        self.match = character
        return character
        
    def append(self, value):
        """
        Append the string to the scanner's text.
        """
        self.text += value
        
    def peek(self, n=1):
        """
        Get the next n characters.
        """
        return self.text[self.pos+1: self.pos+1+n]
    
    def __getitem__(self, value):
        """
        Get a particular character or substring from the underlying text.
        """
        return self.text[value]
    
    @property
    def current_char(self):
        """
        Get the current string. If we are at the end of the text, then return 
        None.  
        """
        if self.end_of_string:
            return None
        else:
            return self.text[self.pos]
      
    @property
    def end_of_string(self):
        """
        Check whether the scanner is at the end of the string.
        """
        return self.pos == len(self.text)
    
    @property
    def rest(self):
        """
        Returns the "rest" of the string. (i.e. everything between the 
        scanner pointer and the end of the string) 
        """
        return self.text[self.pos:]
    
    def __repr__(self):
        max_chars = 30
        return '<{}: position={} text="{}">'.format(
                self.__class__.__name__,
                self.pos,
                self.text[:max_chars] + '...' if len(self.text) > max_chars else self.text)
