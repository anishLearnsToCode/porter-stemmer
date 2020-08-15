#!/usr/bin/env python

"""Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be be regarded
as canonical, in that it follows the algorithm presented in

Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
no. 3, pp 130-137,

only differing from it at the points maked --DEPARTURE-- below.

See also http://www.tartarus.org/~martin/PorterStemmer

The algorithm as described in the paper could be exactly replicated
by adjusting the points of DEPARTURE, but this is barely necessary,
because (a) the points of DEPARTURE are definitely improvements, and
(b) no encoding of the Porter stemmer I have seen is anything like
as exact as this version, even with the points of DEPARTURE!

Vivake Gupta (v@nano.com)

Release 1: January 2001

Further adjustments by Santiago Bruno (bananabruno@gmail.com)
to allow word input not restricted to one word per line, leading
to:

release 2: July 2008
"""

import sys


class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        word is a buffer holding a word to be stemmed. The letters are in the range
        [start, offset ... offset + 1) ... ending at end.
        """
        self.vowels = ('a', 'e', 'i', 'o', 'u')
        self.word = ''
        self.end = 0
        self.start = 0
        self.offset = 0

    def is_vowel(self, letter):
        return letter in self.vowels

    def is_consonant(self, index):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.is_vowel(self.word[index]):
            return False
        if self.word[index] == 'y':
            if index == self.start:
                return True
            else:
                return not self.is_consonant(index - 1)
        return True

    def m(self):
        """m() measures the number of consonant sequences between start and offset.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.start
        while True:
            if i > self.offset:
                return n
            if not self.is_consonant(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.offset:
                    return n
                if self.is_consonant(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.offset:
                    return n
                if not self.is_consonant(i):
                    break
                i += 1
            i += 1

    def contains_vowel(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.start, self.offset + 1):
            if not self.is_consonant(i):
                return 1
        return 0

    def contains_double_consonant(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.start + 1):
            return 0
        if (self.word[j] != self.word[j - 1]):
            return 0
        return self.is_consonant(j)

    def is_of_form_cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.start + 2) or not self.is_consonant(i) or self.is_consonant(i - 1) or not self.is_consonant(i - 2):
            return 0
        ch = self.word[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.word[self.end]:  # tiny speed-up
            return 0
        if length > (self.end - self.start + 1):
            return 0
        if self.word[self.end - length + 1: self.end + 1] != s:
            return 0
        self.offset = self.end - length
        return 1

    def set_to(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.word = self.word[:self.offset + 1] + s + self.word[self.offset + length + 1:]
        self.end = self.offset + length

    def r(self, s):
        """r(s) is used further down. is a mapping function to change morphemes"""
        if self.m() > 0:
            self.set_to(s)

    def remove_plurals(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.word[self.end] == 's':
            if self.ends("sses"):
                self.end = self.end - 2
            elif self.ends("ies"):
                self.set_to("i")
            elif self.word[self.end - 1] != 's':
                self.end = self.end - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.end = self.end - 1
        elif (self.ends("ed") or self.ends("ing")) and self.contains_vowel():
            self.end = self.offset
            if self.ends("at"):
                self.set_to("ate")
            elif self.ends("bl"):
                self.set_to("ble")
            elif self.ends("iz"):
                self.set_to("ize")
            elif self.contains_double_consonant(self.end):
                self.end = self.end - 1
                ch = self.word[self.end]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.end = self.end + 1
            elif self.m() == 1 and self.is_of_form_cvc(self.end):
                self.set_to("e")

    def terminal_y_to_i(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if self.ends('y') and self.contains_vowel():
            self.word = self.word[:self.end] + 'i' + self.word[self.end + 1:]

    def map_double_to_single_suffix(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.word[self.end - 1] == 'a':
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif self.word[self.end - 1] == 'c':
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif self.word[self.end - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.word[self.end - 1] == 'l':
            if self.ends("bli"):
                self.r("ble")  # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif self.word[self.end - 1] == 'o':
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif self.word[self.end - 1] == 's':
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif self.word[self.end - 1] == 't':
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif self.word[self.end - 1] == 'g':  # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.word[self.end] == 'e':
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif self.word[self.end] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.word[self.end] == 'l':
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif self.word[self.end] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.word[self.end - 1] == 'a':
            if self.ends("al"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'c':
            if self.ends("ance"):
                pass
            elif self.ends("ence"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'e':
            if self.ends("er"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'i':
            if self.ends("ic"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'l':
            if self.ends("able"):
                pass
            elif self.ends("ible"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'n':
            if self.ends("ant"):
                pass
            elif self.ends("ement"):
                pass
            elif self.ends("ment"):
                pass
            elif self.ends("ent"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'o':
            if self.ends("ion") and (self.word[self.offset] == 's' or self.word[self.offset] == 't'):
                pass
            elif self.ends("ou"):
                pass
            # takes care of -ous
            else:
                return
        elif self.word[self.end - 1] == 's':
            if self.ends("ism"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 't':
            if self.ends("ate"):
                pass
            elif self.ends("iti"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'u':
            if self.ends("ous"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'v':
            if self.ends("ive"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'z':
            if self.ends("ize"):
                pass
            else:
                return
        else:
            return
        if self.m() > 1:
            self.end = self.offset

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.offset = self.end
        if self.word[self.end] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.is_of_form_cvc(self.end - 1)):
                self.end = self.end - 1
        if self.word[self.end] == 'l' and self.contains_double_consonant(self.end) and self.m() > 1:
            self.end = self.end - 1

    def stem_document(self, document):
        result = []
        for line in document.split('\n'):
            result.append(self.stem_sentence(line))
        return '\n'.join(result)

    def stem_sentence(self, sentence):
        result = []
        for word in sentence.split():
            result.append(self.stem_word(word))
        return ' '.join(result)

    def stem_word(self, word):
        self.word = word
        self.end = len(word) - 1
        self.start = 0

        self.remove_plurals()
        self.terminal_y_to_i()
        self.map_double_to_single_suffix()
        self.step3()
        self.step4()
        self.step5()
        return self.word[self.start: self.end + 1]


if __name__ == '__main__':
    stemmer = PorterStemmer()
    resume = open('resume.txt', 'r').read()
    # print(stemmer.stem_sentence('important links'))
    print(stemmer.stem_document(resume))
