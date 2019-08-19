import sys
import re
import os
import argparse

class MyErrVisualizer():
    """
    Class for Visualizing Python Traceback of Errors
    """

    def __init__(self, err_filepath_lines, n_err=None, cloud_mode=False):
        """
        Initialize Error Visualizer with input error filepath and number of error traces

            Args:
                err_filepath_lines (str, list): File path or File Lines of the Traceback Calls from Python
                n_err (int): Number of traceback calls to be shown, default: 0
                cloud_mode (bool): If Running in Cloud Mode
        """

        if not isinstance(n_err, int) and n_err is not None: raise TypeError('Invalid Type : n_err should be an Integer')
        if not isinstance(err_filepath_lines, (str, list)): raise TypeError('Invalid Type : err_filepath should be a String or a 01List')
        if not isinstance(cloud_mode, bool): raise TypeError('Invalid Type : cloud_mode should be a Boolean')

        self.cloud_mode = cloud_mode
        self.err_filepath_lines = err_filepath_lines
        self.error_lines, self.prime_error = self.getErrorInfo(self.err_filepath_lines, self.cloud_mode)

        self.visualizeErr(n_err=n_err, cloud_mode=self.cloud_mode)
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

    def getErrorInfo(self, err_filepath_lines, cloud_mode):
        """
        Retruns Error Information from the Traceback Calls
        Parses all lines of errors

        Args:
                err_filepath_lines (str, list): File path or File Lines of the Traceback Calls from Python

        Returns:
                error_lines (list): All the Traceback Calls
                prime_error (str): Main Error of this Entire Traceback

        """

        err_file = []

        if cloud_mode:
            err_file = err_filepath_lines

        else:
            if not os.path.isfile(err_filepath_lines):
                print("\n*** File Path Given: {}".format(err_filepath_lines))
                print("*** Invalid File Path! Aborting...")
                # raise Exception("*** Invalid File Path! Aborting...")
                return [], []

            with open(err_filepath_lines) as err_fp:
                err_file = err_fp.readlines()

        err_header = err_file[0].strip()
        err_hdr_macro = "Traceback (most recent call last):"

        if err_header == err_hdr_macro:
            error_lines = [line.strip() for line in err_file[1:]]
            error_lines, prime_error = error_lines[:-1][::-1], error_lines[-1]
            return error_lines, prime_error

        else:
            print("\n*** Header Given: {}".format(err_header))
            print("*** Invalid Error Header! Aborting...")
            # raise Exception("*** Invalid Error Header! Aborting...")
            return [], []


    def visualizeErr(self, n_err=None, cloud_mode=False):
        """
        To Visualize All the Traceback Calls

            Args:
                n_err (int): Number of traceback calls to be shown, default: 0
        """

        if not isinstance(n_err, int) and n_err is not None:
            n_err = None

        if n_err is not None:
            n_err = 0 if n_err <= 0 else n_err

        err_type, err_msg = \
            re.findall(r'(.*):', self.prime_error)[0].strip(), \
            re.findall(r':(.*)', self.prime_error)[0].strip()

        file_paths, line_nos, err_funcs, err_codes = [], [], [], []
        total_count = len(self.error_lines)

        code_to_filepath = {}
        idx_to_code = {}
        idx = 0


        cloud_output = ""

        for err in self.error_lines:
            if err.startswith('File \"'):
                file_path, line_no, err_func = \
                    re.findall(r'File "(.*)"|$, line \d+, in .*', err)[0], \
                    re.findall(r'File ".*", line (\d+)|$, in .*', err)[0], \
                    re.findall(r'File ".*", line \d+, in (.*)|$', err)[0]

                file_paths.append(re.sub(os.path.expanduser("~")+'/',"~/", file_path)), line_nos.append(line_no), err_funcs.append(err_func)

                new_file_info = [re.sub(os.path.expanduser("~")+'/',"~/", file_path),
                                           line_no, err_func]

                code = idx_to_code[idx]
                prev_files_info = code_to_filepath.get(code,[])

                code_to_filepath[code] = prev_files_info + [new_file_info] \
                                            if prev_files_info != [] \
                                            else [new_file_info]

            else:
                idx += 1
                err_codes.append(err)
                idx_to_code[idx] = "{} --- {}".format(idx, err)

        total_count = total_count//2
        n_err = (None if n_err >= (total_count+1)//2 and n_err != 0 else n_err) if (n_err is not None) else n_err

        red, end = '\033[91;1m', '\033[0;0m'
        highlight, bold, underline = '\033[7m', '\033[1m', '\033[4m'


        if len(file_paths) == len(err_codes):
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

            cloud_output += '<b class="errHeading">'+"<br>{}</b>".format("<err_tag>"+err_type +" -> "+ err_msg+"</err_tag>")

            for (level, (fp, el, ef, ec)) in enumerate(zip(file_paths, line_nos, err_funcs, err_codes)):

                if n_err and level%(n_err)==0 and level!=0:
                    print(("\n"+"   "*(level+1)+".")*3 +"\n")

                    cloud_output += ("\n"+"   "*(level+1)+".")*3 +"\n"

                print(" \n{}{} \n{}{} @ {}".format("   "*level,
                                                 highlight+" "+ec+" "+end,
                                                 "   "*level,
                                                 bold+"Line "+ el +": "+ ef +end,
                                                 underline+ fp +end))

                cloud_output += " <br><br>{}{} <br>{}{} @ {}".format(" &emsp; "*level,
                                                 "<mark>"+" "+ec+" "+"</mark>",
                                                 " &emsp; "*level,
                                                 "<b>"+"Line "+ el +": "+ ef +"</b>",
                                                 "<u>"+ fp +"</u>")

            print(red+"-"*(len(prime_err_msg) - (len(end)+len(red)))+end+"\n")

        else:
            prime_err_msg = red+err_type +" -> "+ err_msg+end
            print(red+"-"*(len(prime_err_msg) - (len(end)+len(red)))+end)
            print("{}".format(prime_err_msg))

            cloud_output += '<b class="errHeading">'+"<br>{}</b>".format("<err_tag>"+err_type +" -> "+ err_msg+"</err_tag>")

            levels = min(idx, n_err) if n_err is not None else idx

            for ix in range(levels):
                ec = idx_to_code[ix+1]

                files_info = code_to_filepath[ec]

                ec = ec.split("{} --- ".format(ix+1))[1]

                print(" \n{}{}".format(
                        "   "*ix, highlight+" "+ec+" "+end))

                cloud_output += " <br><br>{}{}".format(
                        " &emsp; "*ix, "<mark>"+" "+ec+" "+"</mark>")

                for (fp, el, ef) in files_info:
                    print("{}{} @ {}".format(
                        "   "*ix,bold+"Line "+ el +": "+ ef +end,
                        underline+ fp +end))

                    cloud_output += "{}{} @ {}".format(
                        " &emsp; "*ix,"<b>"+"Line "+ el +": "+ ef +"</b>",
                        "<u>"+ fp +"</u>")

            print(red+"-"*(len(prime_err_msg) - (len(end)+len(red)))+end+"\n")

        if cloud_mode:
            print("\n\n\n\n #############")
            print(cloud_output)

            self.cloud_output = cloud_output

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--err_file_path', help='Error File Path having the Traceback Calls', required=True)
    parser.add_argument('-n', '--num_calls', help='Number of Traceback Calls', type=int)

    """ Sample Usage """
    # python myErrVisualizer.py
    # -f "sample_err.err" \
    # -n 5

    # python myErrVisualizer.py
    # --err_filepath "sample_err.err" \
    # --num_calls 5


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    if not args.err_file_path:
        err_filepath = ''
    else:
        err_filepath = args.err_file_path

    if args.num_calls is None:
        num_calls = None
    else:
        num_calls = args.num_calls


    # """ Breakpoint """
    # sys.exit(1)

    MyErrVisualizer(err_filepath, num_calls)
