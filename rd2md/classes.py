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

import io
import re


class Documentation:
    def __init__(self, is_class):
        self.name = None
        self.title = None
        self.usage = None
        self.args = []
        self.value = None
        self.description = None
        self.examples = None
        self.is_class = is_class
        self.method_links = []
        self.methods = []

    def add_method(self, method):
        self.methods.append(method)

    def set_name(self, name):
        self.name = name

    def set_title(self, title):
        self.title = title

    def set_usage(self, usage):
        self.usage = usage

    def set_value(self, value):
        self.value = value

    def set_description(self, description):
        self.description = description

    def set_examples(self, examples):
        from .parser import remove_function_call

        examples = remove_function_call("\\dontrun{", examples)
        examples = examples.strip()
        self.examples = examples

    def add_method_link(self, link_text):
        self.method_links.append(link_text)

    def set_args(self, args):
        self.args = args

    def generate(self, file_out):
        with open(file_out, "w") as fp_out:
            if self.is_class:
                if self.description:
                    fp_out.write("## Description\n\n")
                    fp_out.write("%s\n\n" % self.description)
                if self.examples:
                    fp_out.write("## Examples\n\n")
                    fp_out.write("```r\n%s\n```\n\n" % self.examples)
                if self.method_links:
                    fp_out.write("## Methods\n\n")
                    fp_out.write("### Public Methods\n\n")
                    for link_text in self.method_links:
                        link, text = link_text
                        fp_out.write("* [`%s`](%s)\n" % (text, link))
                    fp_out.write("\n")
                if self.methods:
                    for method in self.methods:
                        method.generate(fp_out)
            else:
                if self.name:
                    fp_out.write("# `%s`\n\n" % self.name)
                if self.title:
                    fp_out.write("%s\n\n" % self.title)
                if self.description:
                    fp_out.write("## Description\n\n")
                    fp_out.write("%s\n\n" % self.description)
                if self.usage:
                    fp_out.write("## Usage\n\n")
                    fp_out.write("```r\n")
                    fp_out.write("%s" % self.usage)
                    fp_out.write("```\n\n")
                if self.args:
                    fp_out.write("## Arguments\n\n")
                    fp_out.write("Argument      |Description\n")
                    fp_out.write("------------- |----------------\n")
                    for arg, description in self.args:
                        fp_out.write("`%s` | %s\n" % (arg, description))
                    fp_out.write("\n")
                if self.value:
                    fp_out.write("## Return Value\n\n")
                    fp_out.write("%s\n\n" % self.value)
                if self.examples:
                    fp_out.write("## Examples\n\n")
                    fp_out.write("```r\n%s\n```\n\n" % self.examples)


class Method:
    def __init__(self, link_name, method_name):
        self.link_name = link_name
        self.method_name = method_name
        self.usage = ""
        self.preamble = ""
        self.examples = ""
        self.arguments = ""
        self.returns = ""

    def set_preamble(self, preamble):
        self.preamble = preamble

    def set_examples(self, examples):
        from .parser import remove_function_call

        if "preformatted" not in examples:
            raise Exception("malformed examples; no preformmatted")
        examples = examples.replace("\\if{html}{\\out{</div>}}", "")
        match = re.match(".*preformatted{(.*)}", examples, re.DOTALL)
        groups = match.groups()
        code = groups[0]
        code = remove_function_call("\\dontrun{", code)
        self.examples = code.strip()

    def set_returns(self, returns):
        self.returns = returns

    def set_usage(self, usage):
        if "preformatted" not in usage:
            raise Exception("malformed usage; no preformmatted")
        usage = usage.replace("\\if{html}{\\out{</div>}}", "")
        match = re.match(".*preformatted{(.*)}", usage, re.DOTALL)
        groups = match.groups()
        code = groups[0]
        self.usage = code

    def set_describe(self, describe):
        from .parser import get_curly_contents

        arguments = ""
        fp = io.StringIO(describe)
        line = fp.readline()
        while line:
            if line.startswith("\\item{"):
                arg, desc = get_curly_contents(2, line[5:], fp)
                desc = desc.replace("\n", " ")
                arguments += "* %s %s\n" % (arg, desc)
            else:
                pass  # newlines
            line = fp.readline()
        self.arguments = arguments

    def generate(self, fp_out):
        fp_out.write('<a id="%s"></a>\n' % self.link_name)
        fp_out.write("### %s\n\n" % self.method_name)
        if self.preamble:
            fp_out.write("%s\n\n" % self.preamble)
        if self.usage:
            fp_out.write("<b>Usage</b>\n\n")
            fp_out.write("```r\n")
            fp_out.write("%s\n" % self.usage)
            fp_out.write("```\n\n")
        if self.arguments:
            fp_out.write("<b>Arguments:</b>\n\n")
            fp_out.write("%s\n\n" % self.arguments)
        if self.examples:
            fp_out.write("<b>Example:</b>\n\n")
            fp_out.write("```r\n")
            fp_out.write("%s\n" % self.examples)
            fp_out.write("```\n\n")
        if self.returns:
            fp_out.write("<b>Returns:</b>\n\n")
            fp_out.write("%s\n\n" % self.returns)
