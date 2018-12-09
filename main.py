# [START app]
import logging
import itertools as itr
from flask import Flask, render_template, request, jsonify
# [END imports]


def permute(lst, num):
    return [''.join(a) for a in list(itr.permutations(lst, num))]


def loadWords():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def foundWords(samples, dictionary):
    "returns a list words in samples found in dictionary."
    return [w for w in samples if w in dictionary]


def nWordsFromList(n, char_list):
    dictionary = loadWords()
    return foundWords(permute(char_list, n), dictionary)


def nWordsPos(n, char_list, char, pos):
    word_list = nWordsFromList(n, char_list)
    # found_words = []
    return [w for w in word_list if w[pos - 1] == char]
    # return None


# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/')
def hello():
    return render_template('home.html')


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#    return jsonify({'tasks': tasks})


@app.route('/nwords', methods=['GET'])
def get_nWords():
    try:
        char_list = [c for c in request.args.get('chars').lower()]

        def nPos(n, char, pos):
            return nWordsPos(n, char_list, char, pos)

        def nWords(n):
            return nWordsFromList(n, char_list)

        def nPos2(n, c1, p1, c2, p2):
            word_list = list(set(nPos(n, c1, p1)))
            return [w for w in word_list if w[p2 - 1] == c2]

        try:
            word_size = int(request.args.get('n'))
            try:
                c1 = request.args.get('c1')
                p1 = int(request.args.get('p1'))
                try:
                    c2 = request.args.get('c2')
                    p2 = int(request.args.get('p2'))
                    return jsonify({'chars': char_list,
                                    'word size': word_size,
                                    'words': list(set([w.upper() for w in nPos2(word_size, c1, p1, c2, p2)]))})
                except:
                    return jsonify({'chars': char_list,
                                    'word size': word_size,
                                    'words': list(set([w.upper() for w in nPos(word_size,
                                                                               c1, p1)]))})
            except:
                return jsonify({'chars': char_list,
                                'word size': word_size,
                                'words': list(set([w.upper() for w in nWords(word_size)]))})
        except:
            return jsonify({'chars': char_list,
                            'words': list(set([w.upper() for w in nWords(6)]))})
    except:
        return 'An internal error occurred.', 500

# [START form]


@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)


# j63fresh
