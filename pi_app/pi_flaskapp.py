"""
PI Computation by Binary Splitting Algorithm with GMP libarary
"""
import math
import itertools
from gmpy2 import mpz, isqrt
from time import time, sleep
from flask import Flask, send_file
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

input_digits = api.model(
    'Digits', {'digits': fields.Integer('Number of required decimal digits')})
cache_data = {}


@api.route('/pi_job')
class PiChudnovsky(Resource):
    A = 13591409
    B = 545140134
    C = 640320
    D = 426880
    E = 10005
    C3_24 = C ** 3 // 24
    DIGITS_PER_TERM = math.log(53360 ** 3) / \
        math.log(10)  # => 14.181647462725476

    @api.expect(input_digits)
    def post(self):
        """ Initialization

        :param int digits: digits of PI computation
        """
        try:
            self.digits = api.payload
            self.job_id = generate_id().id
            self.n = math.floor(self.digits / self.DIGITS_PER_TERM + 1)
            self.prec = math.floor((self.digits + 1) * math.log2(10))
            self.tm_s = time()
            cache_data[self.job_id] = (
                self.digits, self.tm_s, 0.0, 'In-progress')
            self.compute()
            return {'success': True, 'job_id': self.job_id}
        except Exception as es:
            return {'success': False, 'error': es.text()}

    def compute(self):
        """ Computation """
        try:
            p, q, t = self.__bsa(0, self.n)
            one_sq = mpz(10) ** (2 * self.digits)
            sqrt_c = isqrt(self.E * one_sq)
            pi = (q * self.D * sqrt_c) // t
            FILENAME = "pi_{}.txt".format(self.job_id)
            pi_val = "{}.{}".format((str(pi))[0], (str(pi))[1:])
            with open(FILENAME, "w") as f:
                f.write(pi_val)
            cache_data[self.job_id] = (self.digits, self.tm_s, pi, 'complete')

        except Exception as e:
            raise

    def __bsa(self, a, b):
        """ PQT computation by BSA(= Binary Splitting Algorithm)

        :param int n1: positive integer
        :param int n2: positive integer
        """
        try:
            if a + 1 == b:
                if a == 0:
                    p_ab = q_ab = mpz(1)
                else:
                    p_ab = mpz((6 * a - 5) * (2 * a - 1) * (6 * a - 1))
                    q_ab = mpz(a * a * a * self.C3_24)
                t_ab = p_ab * (self.A + self.B * a)
                if a & 1:
                    t_ab = -t_ab
            else:
                m = (a + b) // 2
                p_am, q_am, t_am = self.__bsa(a, m)
                p_mb, q_mb, t_mb = self.__bsa(m, b)
                p_ab = p_am * p_mb
                q_ab = q_am * q_mb
                t_ab = q_mb * t_am + p_am * t_mb
            return [p_ab, q_ab, t_ab]

        except Exception as e:
            raise


class generate_id(object):
    id_gen = itertools.count()

    def __init__(self):
        self.id = next(self.id_gen)


@api.route('/pi_job/<job_id>')
@api.doc(responses={'201': 'request created', '400': 'invalid request', '500': 'internal server error'})
class getProgress(Resource):
    def get(self, job_id):
        try:
            if cache_data[int(job_id)][3] == 'In-progress':
                time_elapsed = '{} seconds'.format(
                    round(time() - cache_data[int(job_id)][1]))
                return {'success': True,
                        'job_id': job_id,
                        'digits': cache_data[int(job_id)][0],
                        'status': cache_data[int(job_id)][3],
                        'time_elapsed': time_elapsed}
            else:
                return {'success': True,
                        'job_id': job_id,
                        'digits': cache_data[int(job_id)][0],
                        'status': cache_data[int(job_id)][3]}
        except KeyError:
            return {'success': False,
                    'job_id': job_id,
                    'error': 'Job does not exist'}


@api.route('/download_pi_job/<job_id>')
@api.doc(responses={'201': 'request created', '400': 'invalid request', '500': 'internal server error'})
class download_pi_job(Resource):
    def get(self, job_id):
        path = "pi_{}.txt".format(job_id)
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
