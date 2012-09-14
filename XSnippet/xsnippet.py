# coding: utf-8
#
# Copyright 2012 Igor Kalnitsky <igor@kalnitsky.org>
#
# This file is part of Sublime-XSnippet.
#
# Sublime-XSnippet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sublime-XSnippet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sublimetext-xsnippet.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import json
import urllib
import urllib2

import sublime
from sublime_plugin import TextCommand


def post_to_xsnippet(title, language, content):
    '''
        Send file to xsnippet.org and return link to last one.
        Return 'None' if error occured.
    '''
    POST_SNIPPET_URL = 'http://xsnippet.org/api/v1/snippets/'
    SHOW_SNIPPET_URL = 'http://xsnippet.org/{id}/'

    if not content:
        return None

    data = {'content': content}

    if title is not None:
        data['title'] = title
    if language is not None:
        data['language'] = language

    request = urllib2.Request(POST_SNIPPET_URL, urllib.urlencode(data))
    response = urllib2.urlopen(request)

    if response.getcode() == 201:
        id = json.loads(response.read()).get('id')
        return SHOW_SNIPPET_URL.format(id=id)
    return None


class PostToXsnippetCommand(TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            # get snippet's title
            title = None
            if self.view.file_name():
                title = os.path.basename(self.view.file_name())

            # get snippet's language
            language = self.get_language()

            # get snippet's content
            if region.empty():
                region = sublime.Region(0, self.view.size())
            content = self.view.substr(region)

            # post snippet
            snippeturl = post_to_xsnippet(title, language, content)
            if snippeturl is None:
                continue

            sublime.set_clipboard(snippeturl)
            sublime.status_message('Posted to {link}'.format(link=snippeturl))

    def get_language(self):
        syntaxes = {
            'ActionScript.tmLanguage': 'actionscript',
            'AppleScript.tmLanguage': 'applescript',
            'ASP.tmLanguage': 'asp',
            'Batch File.tmLanguage': 'bat',
            'Bibtex.tmLanguage': 'bibtex',
            'C.tmLanguage': 'c',
            'C#.tmLanguage': 'csharp',
            'C++.tmLanguage': 'cpp',
            'Clojure.tmLanguage': 'clojure',
            'CoffeeScript.tmLanguage': 'coffeescript',
            'CSS.tmLanguage': 'css',
            'D.tmLanguage': 'd',
            'Diff.tmLanguage': 'diff',
            'DOT.tmLanguage': 'dot',
            'Erlang.tmLanguage': 'erlang',
            'Go.tmLanguage': 'go',
            'Groovy.tmLanguage': 'groovy',
            'Haskell.tmLanguage': 'haskell',
            'HTML.tmLanguage': 'html+php',
            'Java.tmLanguage': 'java',
            'JavaScript.tmLanguage': 'javascript',
            'JSON.tmLanguage': 'json',
            'JSON Generic Array Elements.tmLanguage': 'json',
            'LaTeX.tmLanguage': 'latex',
            'LaTeX Beamer.tmLanguage': 'latex',
            'LaTeX Memoir.tmLanguage': 'latex',
            'Lisp.tmLanguage': 'common-lisp',
            'Literate Haskell.tmLanguage': 'haskell',
            'Lua.tmLanguage': 'lua',
            'Makefile.tmLanguage': 'make',
            'Matlab.tmLanguage': 'matlab',
            'Objective-C.tmLanguage': 'objc',
            'Objective-C++.tmLanguage': 'objc',
            'OCaml.tmLanguage': 'ocaml',
            'OCamllex.tmLanguage': 'ocaml',
            'OCamlyacc.tmLanguage': 'ocaml',
            'Perl.tmLanguage': 'perl',
            'PHP.tmLanguage': 'php',
            'Plain text.tmLanguage': 'text',
            'Python.tmLanguage': 'python',
            'R.tmLanguage': 'splus',
            'R Console.tmLanguage': 'rconsole',
            'Regular Expressions (Python).tmLanguage': 'python',
            'Ruby.tmLanguage': 'ruby',
            'Ruby Haml.tmLanguage': 'ruby',
            'Ruby on Rails.tmLanguage': 'ruby',
            'Scala.tmLanguage': 'scala',
            'SCSS.tmLanguage': 'css',
            'Shell-Unix-Generic.tmLanguage': 'bash',
            'SQL.tmLanguage': 'sql',
            'SQL (Rails).tmLanguage': 'sql',
            'Tcl.tmLanguage': 'tcl',
            'TeX.tmLanguage': 'latex',
            'TeX Math.tmLanguage': 'latex',
            'Textile.tmLanguage': 'latex',
            'XML.tmLanguage': 'xml',
            'YAML.tmLanguage': 'yaml'
        }

        language = self.view.settings().get('syntax').split('/')[-1]
        return syntaxes.get(language, None)
