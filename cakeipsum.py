# coding=utf-8

import re
import string

import faker
from faker.generator import random
from faker.utils.distribution import choice_distribution


_re_hash = re.compile(r'#')
_re_perc = re.compile(r'%')
_re_excl = re.compile(r'!')
_re_at = re.compile(r'@')
_re_qm = re.compile(r'\?')


class BaseProvider(object):

    __provider__ = 'base'
    __lang__ = None

    def __init__(self, generator):
        self.generator = generator

    @classmethod
    def random_int(cls, min=0, max=9999):
        """
        Returns a random integer between two values.

        :param min: lower bound value (inclusive; default=0)
        :param max: upper bound value (inclusive; default=9999)
        :returns: random integer between min and max
        """
        return random.randint(min, max)

    @classmethod
    def random_digit(cls):
        """
        Returns a random digit/number
        between 0 and 9.
        """
        return random.randint(0, 9)

    @classmethod
    def random_digit_not_null(cls):
        """
        Returns a random non-zero digit/number
        between 1 and 9.
        """
        return random.randint(1, 9)

    @classmethod
    def random_digit_or_empty(cls):
        """
        Returns a random digit/number
        between 0 and 9 or an empty string.
        """
        if random.randint(0, 1):
            return random.randint(0, 9)
        else:
            return ''

    @classmethod
    def random_digit_not_null_or_empty(cls):
        """
        Returns a random non-zero digit/number
        between 1 and 9 or and empty string.
        """
        if random.randint(0, 1):
            return random.randint(1, 9)
        else:
            return ''

    @classmethod
    def random_number(cls, digits=None, fix_len=False):
        """
        Returns a random number with 1 digit (default, when digits==None),
        a random number with 0 to given number of digits, or a random number
        with given number to given number of digits (when ``fix_len==True``).

        :param digits: maximum number of digits
        :param fix_len:  should the number have fixed length?
        :returns: random number with 0 to given number of digits or
            fixed length number
        """
        if digits is None:
            digits = BaseProvider.random_digit()
        if fix_len:
            return random.randint(pow(10, digits - 1), pow(10, digits) - 1)
        else:
            return random.randint(0, pow(10, digits) - 1)

    @classmethod
    def random_letter(cls):
        """Returns a random letter (between a-z and A-Z)."""
        return random.choice(getattr(string, 'letters', string.ascii_letters))

    @classmethod
    def random_element(cls, elements=('a', 'b', 'c')):
        """
        Returns a random element from a passed object.

        If `elements` is a dictionary, the value will be used as
        a weighting element. For example::

            random_element({"{{variable_1}}": 0.5, "{{variable_2}}": 0.2, "{{variable_3}}": 0.2, "{{variable_4}}": 0.1})

        will have the following distribution:
            * `variable_1`: 50% probability
            * `variable_2`: 20% probability
            * `variable_3`: 20% probability
            * `variable_4`: 10% probability

        """

        if isinstance(elements, dict):
            choices = elements.keys()
            probabilities = elements.values()
            return choice_distribution(list(choices), list(probabilities))
        else:
            return random.choice(list(elements))

    @classmethod
    def random_sample(cls, elements=('a', 'b', 'c'), length=None):
        if length is None:
            length = random.randint(1, len(elements))

        return [cls.random_element(elements) for _ in range(length)]

    @classmethod
    def random_sample_unique(cls, elements=('a', 'b', 'c'), length=None):
        """
        Returns a `set` of random unique elements for the specified length.
        """
        if length is None:
            length = random.randint(1, len(elements))

        if length > len(elements):
            raise ValueError("Sample length cannot be longer than the number of elements to pick from.")
        sample = set()
        while len(sample) < length:
            sample.add(cls.random_element(elements))
        return sample

    @classmethod
    def randomize_nb_elements(cls, number=10, le=False, ge=False):
        """
        Returns a random value near number.

        :param number: value to which the result must be near
        :param le: result must be lower or equal to number
        :param ge: result must be greater or equal to number
        :returns: a random int near number
        """
        if le and ge:
            return number
        _min = 100 if ge else 60
        _max = 100 if le else 140
        return int(number * random.randint(_min, _max) / 100) + 1

    @classmethod
    def numerify(cls, text='###'):
        """
        Replaces all placeholders in given text with randomized values,
        replacing: all hash sign ('#') occurrences with a random digit
        (from 0 to 9); all percentage sign ('%') occurrences with a
        random non-zero digit (from 1 to 9); all exclamation mark ('!')
        occurrences with a random digit (from 0 to 9) or an empty string;
        and all at symbol ('@') occurrences with a random non-zero digit
        (from 1 to 9) or an empty string.

        :param text: string to be parsed
        :returns: string with all numerical placeholders filled in
        """
        text = _re_hash.sub(
            lambda x: str(BaseProvider.random_digit()),
            text)
        text = _re_perc.sub(
            lambda x: str(BaseProvider.random_digit_not_null()),
            text)
        text = _re_excl.sub(
            lambda x: str(BaseProvider.random_digit_or_empty()),
            text)
        text = _re_at.sub(
            lambda x: str(BaseProvider.random_digit_not_null_or_empty()),
            text)
        return text

    @classmethod
    def lexify(cls, text='????'):
        """
        Replaces all question mark ('?') occurrences with a random letter.

        :param text: string to be parsed
        :returns: string with all letter placeholders filled in
        """
        return _re_qm.sub(lambda x: BaseProvider.random_letter(), text)

    @classmethod
    def bothify(cls, text='## ??'):
        """
        Replaces all placeholders with random numbers and letters.

        :param text: string to be parsed
        :returns: string with all numerical and letter placeholders filled in
        """
        return BaseProvider.lexify(BaseProvider.numerify(text))

#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################




localized = True




class LoremProvider(BaseProvider):
    word_connector = ' '
    sentence_punctuation = '.'
    @classmethod
    def word(cls):
        """
        Generate a random word
        :example 'lorem'
        """
        return cls.random_element(cls.word_list)

    @classmethod
    def words(cls, nb=3):
        """
        Generate an array of random words
        :example array('Lorem', 'ipsum', 'dolor')
        :param nb how many words to return
        """
        return [cls.word() for _ in range(0, nb)]

    @classmethod
    def sentence(cls, nb_words=6, variable_nb_words=True):
        """
        Generate a random sentence
        :example 'Lorem ipsum dolor sit amet.'
        :param nb_words around how many words the sentence should contain
        :param variable_nb_words set to false if you want exactly $nbWords returned,
            otherwise $nbWords may vary by +/-40% with a minimum of 1
        """
        if nb_words <= 0:
            return ''

        if variable_nb_words:
            nb_words = cls.randomize_nb_elements(nb_words)

        words = cls.words(nb_words)
        words[0] = words[0].title()

        return cls.word_connector.join(words) + cls.sentence_punctuation

    @classmethod
    def sentences(cls, nb=3):
        """
        Generate an array of sentences
        :example array('Lorem ipsum dolor sit amet.', 'Consectetur adipisicing eli.')
        :param nb how many sentences to return
        :return list
        """
        return [cls.sentence() for _ in range(0, nb)]

    @classmethod
    def paragraph(cls, nb_sentences=3, variable_nb_sentences=True):
        """
        Generate a single paragraph
        :example 'Sapiente sunt omnis. Ut pariatur ad autem ducimus et. Voluptas rem voluptas sint modi dolorem amet.'
        :param nb_sentences around how many sentences the paragraph should contain
        :param variable_nb_sentences set to false if you want exactly $nbSentences returned,
            otherwise $nbSentences may vary by +/-40% with a minimum of 1
        :return string
        """
        if nb_sentences <= 0:
            return ''

        if variable_nb_sentences:
            nb_sentences = cls.randomize_nb_elements(nb_sentences)

        return cls.word_connector.join(cls.sentences(nb_sentences))

    @classmethod
    def paragraphs(cls, nb=3):
        """
        Generate an array of paragraphs
        :example array($paragraph1, $paragraph2, $paragraph3)
        :param nb how many paragraphs to return
        :return array
        """
        return [cls.paragraph() for _ in range(0, nb)]

    @classmethod
    def text(cls, max_nb_chars=200):
        """
        Generate a text string.
        Depending on the $maxNbChars, returns a string made of words, sentences, or paragraphs.
        :example 'Sapiente sunt omnis. Ut pariatur ad autem ducimus et. Voluptas rem voluptas sint modi dolorem amet.'
        :param max_nb_chars Maximum number of characters the text should contain (minimum 5)
        :return string
        """
        text = []
        if max_nb_chars < 5:
            raise ValueError('text() can only generate text of at least 5 characters')

        if max_nb_chars < 25:
            # join words
            while not text:
                size = 0
                # determine how many words are needed to reach the $max_nb_chars once;
                while size < max_nb_chars:
                    word = (cls.word_connector if size else '') + cls.word()
                    text.append(word)
                    size += len(word)
                text.pop()
            text[0] = text[0][0].upper() + text[0][1:]
            last_index = len(text) - 1
            text[last_index] += cls.sentence_punctuation
        elif max_nb_chars < 100:
            # join sentences
            while not text:
                size = 0
                # determine how many sentences are needed to reach the $max_nb_chars once
                while size < max_nb_chars:
                    sentence = (cls.word_connector if size else '') + cls.sentence()
                    text.append(sentence)
                    size += len(sentence)
                text.pop()
        else:
            # join paragraphs
            while not text:
                size = 0
                # determine how many paragraphs are needed to reach the $max_nb_chars once
                while size < max_nb_chars:
                    paragraph = ('\n' if size else '') + cls.paragraph()
                    text.append(paragraph)
                    size += len(paragraph)
                text.pop()

        return "".join(text)

########################################################################3
########################################################################3
########################################################################3
########################################################################3
########################################################################3
########################################################################3
########################################################################3

class CakeIpsum(LoremProvider):
    word_list = ['danish',
 'cheesecake.',
 'sugar',
 'Lollipop',
 'wafer',
 'Gummies',
 'apple',
 'Macaroon',
 'roll',
 'roll.',
 'muffin',
 'claw.',
 'Caramels',
 'jelly-o.',
 'Gingerbread',
 'Sugar',
 'Icing',
 'marzipan.',
 'lemon',
 'Pudding',
 'carrot',
 'drops',
 'canes.',
 'cotton',
 'cake',
 'bonbon',
 'gingerbread',
 'cookie.',
 'tootsie',
 'canes',
 'snaps.',
 'croissant',
 'Sweet',
 'Dragée',
 'toffee',
 'chups',
 'marzipan',
 'macaroon',
 'Topping',
 'cheesecake',
 'jujubes.',
 'jelly-o',
 'Cupcake',
 'cupcake',
 'soufflé.',
 'marshmallow',
 'Danish',
 'drops.',
 'bears',
 'ice',
 'Apple',
 'sesame',
 'Jelly',
 'beans',
 'croissant.',
 'chocolate.',
 'dragée.',
 'Cotton',
 'gummies',
 'gummi',
 'beans.',
 'Cake',
 'brownie',
 'Pie',
 'Carrot',
 'topping',
 'Oat',
 'tiramisu',
 'dessert',
 'sweet',
 'plum.',
 'Liquorice',
 'chups.',
 'pastry',
 'Wafer',
 'jelly.',
 'Donut',
 'powder',
 'donut.',
 'Brownie',
 'chocolate',
 'Candy',
 'tiramisu.',
 'candy.',
 'cookie',
 'bar',
 'biscuit.',
 'Jelly-o',
 'soufflé',
 'Dessert',
 'lollipop',
 'Chocolate',
 'jelly',
 'plum',
 'toffee.',
 'lollipop.',
 'cream.',
 'snaps',
 'tart',
 'candy',
 'claw',
 'Biscuit',
 'icing.',
 'Croissant',
 'Marzipan',
 'liquorice',
 'Jujubes',
 'caramels',
 'fruitcake',
 'cream',
 'pudding',
 'cake.',
 'powder.',
 'Toffee',
 'Chupa',
 'dragée',
 'jujubes',
 'Marshmallow',
 'halvah',
 'bear',
 'halvah.',
 'biscuit',
 'donut',
 'icing',
 'chupa',
 'pie',
 'bar.',
 'Ice',
 'oat']

if __name__ == "__main__":
    print(CakeIpsum.paragraph())