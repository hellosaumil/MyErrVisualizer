import re
import os

class MyErrVisualizer():
    """
    Class for Visualizing Python Traceback of Errors 
    """
    
    def __init__(self, err_filepath, n_err=0):   
        """
        Initialize Error Visualizer with input error filepath and number of error traces

            Args:
                err_filepath (str): File path to the Traceback Calls from Python
                n_err (int): Number of traceback calls to be shown, default: 0
        """
        
        if not isinstance(n_err, int): raise TypeError('Invalid Type : n_err should be an Integer')
        if not isinstance(err_filepath, str): raise TypeError('Invalid Type : err_filepath should be a String')
    
        self.err_file_path = err_filepath
        self.error_lines, self.prime_error = self.getErrorInfo(self.err_file_path)
        
        self.visualizeErr(n_err=n_err)
        pass

    def __str__(self):
        """
        Retruns Number of Total Traceback Calls
        """
        return "Total {} callbacks".format(len(self))
    
    def __len__(self):
        """
        Retruns Total Count Traceback Calls
        """
        return len(self.error_lines) // 2

    def getErrorInfo(self, err_filepath):
        """
        Retruns Error Information from the Traceback Calls
        Parses all lines of errors
        
        Args:
                err_filepath (str): File path to the Traceback Calls from Python
    
        Returns:
                error_lines (list): All the Traceback Calls 
                prime_error (str): Main Error of this Entire Traceback
        
        """
        
        if not os.path.isfile(err_filepath):
            print("\n*** File Path Given: {}".format(err_filepath))
            print("*** Invalid File Path! Aborting...")
            # raise Exception("*** Invalid File Path! Aborting...")
            return [], []

        with open(err_filepath) as err_file:
            err_header = err_file.readline().strip()
            err_hdr_macro = "Traceback (most recent call last):"

            if err_header == err_hdr_macro:
                error_lines = [line.strip() for line in err_file]
                error_lines, prime_error = error_lines[:-1], error_lines[-1]
            else:
                print("\n*** Header Given: {}".format(err_header))
                print("*** Invalid Error Header! Aborting...")
                # raise Exception("*** Invalid Error Header! Aborting...")
                return [], []
            
            return error_lines, prime_error

    
    def visualizeErr(self, n_err=None):
        """
        To Visualize All the Traceback Calls

            Args:
                n_err (int): Number of traceback calls to be shown, default: 0
        """
            
        if not os.path.isfile(self.err_file_path):
            return None
        
        if not isinstance(n_err, int) and n_err is not None: 
            n_err = None
        
        err_type, err_msg = \
            re.findall(r'(\D+):', prime_error)[0].strip(), \
            re.findall(r':(\D+)', prime_error)[0].strip()
        
        file_paths, line_nos, err_funcs, err_codes = [], [], [], []
        total_count = len(self.error_lines)

        if total_count % 2 == 0:
            for err in self.error_lines:
                if err.startswith("File"):
                    file_path, line_no, err_func = \
                        re.findall(r'File "(.*)", line \d+, in \D+', err)[0], \
                        re.findall(r'File ".*", line (\d+), in \D+', err)[0], \
                        re.findall(r'File ".*", line \d+, in (.*)', err)[0]

                    file_paths.append(re.sub(os.path.expanduser("~")+'/',"~/", file_path)), line_nos.append(line_no), err_funcs.append(err_func)

                else:
                    err_codes.append(err)

        file_paths, line_nos, err_funcs, err_codes = \
                                                    file_paths[::-1], \
                                                    line_nos[::-1], \
                                                    err_funcs[::-1], \
                                                    err_codes[::-1]
        
        total_count = total_count//2
        n_err = (None if n_err >= (total_count+1)//2 and n_err != 0 else n_err) if (n_err is not None) else n_err
        
        if n_err != None:
            file_paths, line_nos, err_funcs, err_codes = \
                                                        file_paths[:n_err]+file_paths[total_count-n_err:], \
                                                        line_nos[:n_err]+line_nos[total_count-n_err:], \
                                                        err_funcs[:n_err]+err_funcs[total_count-n_err:], \
                                                        err_codes[:n_err]+err_codes[total_count-n_err:]
        
        red, end = '\033[91;1m', '\033[0;0m'
        highlight, bold, underline = '\033[7m', '\033[1m', '\033[4m'
            
        prime_err_msg = red+err_type +" -> "+ err_msg+end
        print(red+"-"*(len(prime_err_msg) - (len(end)+len(red)))+end)
        print("{}".format(prime_err_msg))
        
        for (level, (fp, el, ef, ec)) in enumerate(zip(file_paths, line_nos, err_funcs, err_codes)):
            
            if n_err and level%(n_err)==0 and level!=0:
                print(("\n"+"\t"*(level+1)+".")*3 +"\n")
            
            print("\n{}{} @ {} \n{}{}".format("\t"*level, 
                                                highlight+ " "+el+": "+ec+" " +end, 
                                                bold+ ef +end, 
                                                "\t"*level, 
                                                underline+ fp +end))
