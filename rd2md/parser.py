# -*- coding: utf-8 -*-
# ##################################
#   ____                     _     #
#  / ___|___  _ __ ___   ___| |_   #
# | |   / _ \| '_ ` _ \ / _ \ __|  #
# | |__| (_) | | | | | |  __/ |_   #
#  \____\___/|_| |_| |_|\___|\__|  #
#                                  #
#        Copyright (c) 2023        #
#      rd2md Development Team      #
#       All rights reserved        #
####################################

import re

from .classes import Documentation, Method

DEBUG = False


def process_method(doc, link_name, fp):
    # \subsection{Method \code{print()}}{
    line = fp.readline().strip()
    method_name = line[12:-2]
    method_name = clean(method_name)
    method = Method(link_name, method_name)
    char = fp.read(1)
    stack = 1
    text = ""
    # First, get the text:
    while True:
        text += char
        if char == "{":
            stack += 1
        elif char == "}":
            stack -= 1
            if stack == 0:
                break
        char = fp.read(1)
    # Next, we tokenize it:
    tokens = tokenize(clean(text))
    # Now, we parse the subsections:
    preamble = ""
    in_preamble = True
    position = 0
    while position < len(tokens):
        token = tokens[position]
        if token == "\\":
            if tokens[position + 1] == "subsection":
                in_preamble = False
                if tokens[position + 3] == "Usage":
                    position, usage = get_tokenized_section(
                        position + 5, tokens
                    )  # noqa
                    method.set_usage(usage)
                elif tokens[position + 3] == "Arguments":
                    # skip this, we'll get with describe
                    position += 5
                elif tokens[position + 3] == "Examples":
                    position, examples = get_tokenized_section(
                        position + 5, tokens
                    )  # noqa
                    method.set_examples(examples)
                elif tokens[position + 3] == "Returns":
                    position, returns = get_tokenized_section(
                        position + 5, tokens
                    )  # noqa
                    method.set_returns(returns)
                else:
                    raise Exception("unkown subsection:", tokens[position + 3])
            elif tokens[position + 1] == "describe":
                # breakpoint()
                position, describe = get_tokenized_section(position + 2, tokens)  # noqa
                method.set_describe(describe)
            else:
                # \html
                position += 1
        else:
            if in_preamble:
                preamble += token
            position += 1
    # add method to doc
    method.set_preamble(preamble)
    doc.add_method(method)


def get_tokenized_section(position, tokens):
    stack = 0
    retval = ""
    while True:
        token = tokens[position]
        # print("token:", token)
        retval += token
        if token == "{":
            stack += 1
        elif token == "}":
            stack -= 1
        if stack == 0:
            break
        position += 1
    return position, retval[1:-1]


def tokenize(text):
    tokens = []
    current = ""
    for char in text:
        if char in ["}", "{", "\\"]:
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
        else:
            current += char
    if current:
        tokens.append(current)
    return tokens


def remove_function_call(name, text):
    """
    Removes a "function{...}" from text.
    """
    state = None
    current = ""
    stack = 0
    results = ""
    for char in text:
        if state == "inside":
            # look for ending "}" if not inside another {
            if char == "{":
                stack += 1
                current += char
            elif char == "}":
                if stack == 0:
                    results += current
                    state = None
                    current = ""
                else:
                    stack -= 1
                    current += char
            else:
                current += char
        else:
            current += char

        if current[-len(name) :] == name:  # noqa
            # we're starting the function all
            state = "inside"
            results += current[: -len(name)]
            current = ""

    results += current

    return results


def clean(string):
    # \link[=create_experiment]{create_experiment()}
    string = re.sub(
        "\\\\code\{\\\\link\[=([^\]]*?)\]\{([^\}]*?)\}\}", "[`\\2`](../\\1)", string
    )
    # \code{\link{LoggedArtifact}}
    string = re.sub("\\\\code{\\\\link\{([^\}]*?)\}}", "[`\\1`](./\\1)", string)
    # \link{LoggedArtifact}
    string = re.sub("\\\\link\{([^\}]*?)\}", "[\\1](./\\1)", string)
    # Add the code indicator: \code{...}
    string = re.sub("\\\\code\{([^\}]*?)\}", "`\\1`", string)
    return string


def get_char(line, fp):
    if line:
        char = line[0]
        line = line[1:]
    else:
        char = fp.read(1)
    return line, char


def get_curly_contents(number, line, fp):
    retval = []
    count = 0
    current = ""
    while True:
        line, char = get_char(line, fp)
        if char == "}":
            count -= 1
            if count == 0:
                if current.startswith("{"):
                    retval.append(current[1:])
                elif current.startswith("}{"):
                    retval.append(current[2:])
                else:
                    raise Exception("malformed?", current)
                current = ""
        elif char == "{":
            count += 1
        if len(retval) == number:
            return retval
        current += char


def rd2md(file_in, file_out, is_class):
    if DEBUG:
        print(file_in, file_out)
    doc = Documentation(is_class)
    with open(file_in) as fp_in:
        line = fp_in.readline()
        while line:
            line = line.rstrip()
            if line.startswith("%"):
                pass
            elif line.startswith("\\name{"):
                if DEBUG:
                    print(line)
                name = re.search("{(.*)}", line).groups()[0]
                doc.set_name(name)
            elif line.startswith("\\title{"):
                title = re.search("{(.*)}", line).groups()[0]
                doc.set_title(title)
            elif line.startswith("\\usage{"):
                usage = ""
                line = fp_in.readline().rstrip()
                while line != "}":
                    usage += line + "\n"
                    line = fp_in.readline().rstrip()
                doc.set_usage(usage)
            elif line.startswith("\\description{"):
                description = get_curly_contents(1, line[12:], fp_in)[0]
                doc.set_description(clean(description))
            elif line.startswith("\\value{"):
                value = get_curly_contents(1, line[6:], fp_in)[0]
                doc.set_value(clean(value))
            elif line.startswith("\\examples{"):
                examples = get_curly_contents(1, line[9:], fp_in)[0]
                doc.set_examples(clean(examples))
            elif line.startswith("\\item \\href"):
                link, text = line[12:-2].split("}{")
                text = text.replace("\\code{", "")
                doc.add_method_link((link, text))
            elif line == "\\if{html}{\\out{<hr>}}":
                # \if{html}{\out{<a id="method-Experiment-print"></a>}}
                line = fp_in.readline().strip()
                link_name = line[22:-8]
                _ = fp_in.readline().strip()
                process_method(doc, link_name, fp_in)
            elif line.startswith("\\arguments{"):
                args = []
                while line != "}":
                    if line.startswith("\\item{"):
                        text = line[5:] + " "
                        arg, description = get_curly_contents(2, text, fp_in)
                        description = description.replace("\n", " ")
                        args.append((arg, clean(description)))
                    line = fp_in.readline().rstrip()
                doc.set_args(args)
            line = fp_in.readline()
        doc.generate(file_out)
