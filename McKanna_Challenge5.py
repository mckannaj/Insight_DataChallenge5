"""
Please write a program that takes a list of strings containing integers and words and returns a sorted version
of the list. The goal is to sort this list in such a way that all words are in alphabetical order and all integers
are in numerical order. Furthermore, if the nth element in the list is an integer it must remain an integer, and
if it is a word it must remain a word.

In addition, the strings and integers may contain characters that are ascii symbols that neither belong to letter
set nor digit set (i.e. "#", "%", ";", etc). You are required to remove them during the process so that the output
will contain only letters or digits. For example, if a string is "sym*bo+l", the output should be "symbol". If an
integer is "12%3", the output should be "123". You don't have to worry about strings or integers that contain only
non­letter­non­digit characters, like "^!?", "&", etc.

For example: 20 cat bi?rd 12 do@g >> should read >> 12 bird cat 20 dog
"""


class Solution(object):
    def decode_sort(self, f_in, f_out):
        """
        :type f_in: input filename
        :type f_out: output filename
        :rtype: binary

        This takes an input filename of a file containing a string of strings (as described in the
        challenge description) and writes a sorted, cleaned string (as described in the challenge description)
        to the given output filename. If it succeeds, it returns True.
        """
        input_file = open(f_in, 'r')
        input_str = input_file.read()
        input_file.close()
        decoded = self.decode_str(input_str)
        output_file = open(f_out, 'w')
        output_file.write(decoded)
        output_file.close()
        return True

    def decode_str(self, s):
        """
        :type s: str
        :rtype: str

        This takes a string of strings (as described in the challenge description) and returns a sorted, cleaned string
        (as described in the challenge description).
        """
        num_word_order = []
        num_list = []
        word_list = []
        ret_str = ''
        tokenized_list = self.tokenize(s)
        if (len(tokenized_list) < 1): # nothing here; just return (maybe Warn?)
            return s
        if (len(tokenized_list) == 1): # we only have one thing; just clean and return it
            (clean_tok, num_flag) = self.remove_bad_characters(tokenized_list[0])
            return clean_tok

        for tok in tokenized_list:
            (clean_tok, num_flag) = self.remove_bad_characters(tok)
            if (num_flag == 1): # this was an integer
                num_word_order += 'n'
                num_list.append(clean_tok)
            else:
                num_word_order += 'w'
                word_list.append(clean_tok)
        num_list = self.sort_integers(num_list)
        word_list = self.sort_words(word_list)
        for flag in num_word_order:
            if (flag == 'n'): # the next thing should be a number
                ret_str += str(num_list.pop(0)) + ' '
            else:
                ret_str += word_list.pop(0) + ' '
        return ret_str[0:len(ret_str)-1] # remove that last space

    def remove_bad_characters(self, s):
        """
        :type s: str
        :rtype: str

        This takes a string which is either a word or an integer between ­999999 and 999999 which may contain
        non-letter, non-number characters. It removes those characters and returns either the integer or the word.
        It also returns a flag which is 1 if the return is an integer and 0 if it is a word.
        """
        neg_flag = 0
        num_flag = 0
        word_flag = 0
        idx = 0
        ret_str = ''
        if len(s) < 1: # empty string, guess we're already done. Might want to return an error here?
            return s
        else:
            while (idx < len(s)): # go through each character
                if (num_flag + word_flag == 0):  # we don't know which type we're dealing with yet: special case
                    if (s[idx] == '-'):
                        neg_flag = 1 # if it's a number, it's a negative
                    elif (s[idx].isalpha()):
                        word_flag = 1
                        ret_str += s[idx]
                    elif (s[idx].isdigit()):
                        num_flag = 1
                        ret_str += s[idx]
                elif (s[idx].isalnum()): # we know it's a number or a word; just grab the good characters
                    ret_str += s[idx]
                idx += 1
            if (num_flag == 1):
                if (neg_flag == 1):
                    return (int(ret_str) * -1, num_flag)
                else:
                    return (int(ret_str), num_flag)
            else: # just assuming word here, could put error checking in...
                return ret_str, num_flag

            print('Not sure how we got here - should not be possible???')
            return None


    def tokenize(self, s):
        """
        :type s: str
        :rtype: list

        This takes a string of strings separated by single spaces (as described in the challenge description)
        and returns a list of those strings.
        """
        return s.split()

    def sort_integers(self, int_list):
        """
        :type int_list: list
        :rtype: list

        This takes a list of integers and sorts them from lowest to highest, returning a sorted list.
        """
        return sorted(int_list)

    def sort_words(self, word_list):
        """
        :type word_list: list
        :rtype: list

        This takes a list of words and sorts them alphabetically, returning a sorted list.
        """
        return sorted(word_list)



# Some test cases:
import cProfile, pstats

def main():
    s = Solution()
    n_sorted = s.sort_integers([-5, 88, -32498, 12345, 3883, 0, 1927])
    print("Expected return: sorted integers; received {}.".format(n_sorted))

    w_sorted = s.sort_words(['frank','bob','john','harold','jimbles'])
    print("Expected return: alphabetical list; received {} {} {} {} {}.".format(w_sorted[0], w_sorted[1],
                                                                                w_sorted[2], w_sorted[3], w_sorted[4]))

    (clean, flag) = s.remove_bad_characters('4358')
    print("Expected return: 4358; received {}.".format(clean))

    (clean, flag) = s.remove_bad_characters('!!!4358!!!?')
    print("Expected return: 4358; received {}.".format(clean))

    (clean, flag) = s.remove_bad_characters('-12398')
    print("Expected return: -12398; received {}.".format(clean))

    (clean, flag) = s.remove_bad_characters('$-1@$2^3()9!!8#$%')
    print("Expected return: -12398; received {}.".format(clean))

    (clean, flag) = s.remove_bad_characters('doggy')
    print("Expected return: doggy; received {}.".format(clean))

    (clean, flag) = s.remove_bad_characters('-@#$d@#$%o#%^g$^*g(y^&*(&^')
    print("Expected return: doggy; received {}.".format(clean))

    tokens = s.tokenize('!!!4358!!!? $-1@$2^3()9!!8#$% -@#$d@#$%o#%^g$^*g(y^&*(&^')
    print("Expected return: tokenized list; received {}.".format(tokens))

    decoded = s.decode_str('!!!4358!!!? $-1@$2^3()9!!8#$% -@#$d@#$%o#%^g$^*g(y^&*(&^ g@rumples !!!-234 %fl))oppy')
    print("Expected return: decoded list num-num-word-word-num-word; received {}.".format(decoded))

    decoded = s.decode_str('-@#$d@#$%o#%^g$^*g(y^&*(&^')
    print("Expected return: doggy; received {}.".format(decoded))

    decoded = s.decode_str('')
    print("Expected return: None; received {}.".format(decoded))

    decoded = s.decode_str('20 cat bi?rd 12 do@g')
    print("Expected return: 12 bird cat 20 dog; received {}.".format(decoded))

    input_filename = 'DC5_input.txt'
    output_filename = 'DC5_output.txt'
    success = s.decode_sort(input_filename, output_filename)
    print("Expected return: True; received {}.".format(success))


    cProfile.runctx('from McKanna_Challenge5 import Solution; s = Solution(); s.decode_sort("DC5_input.txt", "DC5_output.txt")', {}, {}, filename='stats.txt')
    p = pstats.Stats('stats.txt')
    p.sort_stats('time').print_stats(20)


if __name__ == "__main__":
    main()

