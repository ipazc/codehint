#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#MIT License
#
#Copyright (c) 2017 Iván de Paz Centeno
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from dill.source import getsource

__author__ = 'Iván de Paz Centeno'


def hint(f, do_print=True):
    result = ParseSource(getsource(f)).describe()

    if do_print:
        print(result)

    return result


class ParseSource(object):

    def __init__(self, source):
        self.source = source.split("\n")

    def get_first_comment(self):
        func_code = self.source
        if "\n" in func_code:
            func_code = func_code.split("\n")

        comment = []

        in_comment = False
        finished = False

        # search for comments
        for line in func_code[1:]:
            if finished: break

            stripped_line = line.strip()

            if in_comment:

                if stripped_line.rstrip().endswith('"""'):
                    in_comment = False
                    finished = True
                    stripped_line = stripped_line.rstrip('"""').strip()

                comment.append(stripped_line)

            else:

                if stripped_line == "":
                    continue

                elif stripped_line.startswith("#"):
                    comment.append(stripped_line.lstrip("#").strip())

                elif stripped_line.startswith('"""'):
                    in_comment = True
                    if len(stripped_line) > 3:
                        comment.append(stripped_line.lstrip('"""').strip())

                else:
                    finished = True

        return comment

    def get_header(self):
        if len(self.source) == 0:
            return ""

        header = self.source[0].lstrip()

        return header

    def __params(self, header):
        param_section = header.split("(")[1].split(")")[0]

        arguments = [param.strip() for param in param_section.split(",")]

        args_table = {}
        args_order = []
        for argument in arguments:
            if argument.strip() == "": continue

            splitted_argument = argument.split(":")

            if len(splitted_argument) > 1:
                arg_type = splitted_argument[1]
            else:
                arg_type = "Any"

            arg_name = splitted_argument[0]

            args_table[arg_name] = arg_type
            args_order.append(arg_name)

        result_data = header.split("->")

        if len(result_data) > 1:
            return_type = result_data[1].split(":")[0].strip()
        else:
            return_type = "Any"

        return args_table, args_order, return_type

    def __comment_params(self, header_comment):

        main_desc = ""
        args_desc_table = {}
        last_param = None
        return_info = ""

        for param in header_comment:
            stripped_param = param.strip()

            if stripped_param.startswith(":param"):
                param_split = stripped_param.split(":param", 1)[1]
                param_info = param_split.split(":", 1)
                param_name = param_info[0].strip()
                param_desc = param_info[1]
                args_desc_table[param_name] = param_desc
                last_param = param_name

            elif return_info == "" and stripped_param.startswith(":return"):
                param_split = stripped_param.split(":return", 1)[1]
                param_info = param_split.split(":", 1)[1]
                return_info = param_info

            else:
                if len(return_info) > 0:
                    return_info += " {}".format(stripped_param)
                elif last_param == None:
                    main_desc += " {}".format(stripped_param)
                else:
                    args_desc_table[last_param] += " {}".format(stripped_param)

        return args_desc_table, main_desc.strip(), return_info.strip()

    def describe_header(self, header, header_comment):
        args_table, args_order, return_type = self.__params(header)
        args_comment_table, main_desc, return_info = self.__comment_params(header_comment)

        final_args_table = {arg: {'type': t, 'desc': "Not provided"} for arg, t in args_table.items()}

        for arg, desc in args_comment_table.items():
            if arg in final_args_table:
                final_args_table[arg]['desc'] = desc

        return_table = {'type': return_type, 'desc': return_info}

        return main_desc, final_args_table, args_order, return_table

    def describe(self):
        header = self.get_header()
        comments = self.get_first_comment()

        main_desc, final_args_table, args_order, return_table = self.describe_header(header, comments)

        # Let's pretty-print
        description = "------------------------\n"
        description += header

        description += "\n"

        if len(main_desc.strip()) > 0:
              description += format("\n    {}\n".format(main_desc))

        description += "\n=== Parameters: {} ======".format(len(args_order))

        for arg_index, argument in enumerate(args_order):
            description += "\n [{}] {} (type {}) ->  {}".format(arg_index, argument, final_args_table[argument]['type'], final_args_table[argument]['desc'].strip())

        description += "\n========================" \
                       "\n Result (type {}) ->".format(return_table["type"])

        if return_table['desc'].strip() != "":
            description += "  {}".format(return_table["desc"])

        description += "\n"

        return description

    def __repr__(self):
        return self.describe()

    def __str__(self):
        return self.describe()
