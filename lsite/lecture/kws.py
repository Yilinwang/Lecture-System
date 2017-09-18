import re
from subprocess import Popen, PIPE
import copy
import sys


class kws:
    #def eprint(*args, **kwargs):
    #    print(*args, file=sys.stderr, **kwargs)

    def __init__(self):
        phone_file = './lecture/data/lang/phones.txt'
        lexicon_file = './lecture/data/other/lexicon.txt'
        result_list_file = './lecture/data/other/result_list.txt'
        text_file = './lecture/data/other/text.txt'
        time_file = './lecture/data/other/utt_time.txt'

        self.alpha_re = re.compile('[a-zA-Z]')

        self.phone_lst = []
        with open(phone_file, 'r') as fin:
            for line in fin:
                if line.startswith('EN'):
                    self.phone_lst.append(line.strip().split()[0].split('_')[0])

        self.lex = []
        self.phone2word = {}
        with open(lexicon_file, 'r') as fin:
            for i, line in enumerate(fin):
                line = line.strip().split()
                self.lex.append(line[0])
                if i >= 2 and i < 2179:
                    self.phone2word[' '.join(line[1:])] = line[0]

        self.result_lst = []
        with open(result_list_file, 'r') as fin:
            for line in fin:
                self.result_lst.append(line.strip())

        self.uttid2text = {}
        with open(text_file, 'r') as fin:
            for line in fin:
                line = line.strip().split()
                self.uttid2text[line[0]] = ' '.join(line[1:])

        self.uttid2time = {}
        with open(time_file, 'r') as fin:
            for line in fin:
                line = line.strip().split()
                self.uttid2time[line[0]] = ' '.join(line[1:])


    def search(self, user_query):
        query = ['']
        text = ' '.join(user_query)

        s = ''
        idx = 0
        for c in text:
            if c == ' ':
                if len(s) > 0:
                    query[idx] += s
                    s = ''
                query.append('')
                idx += 1
            elif self.alpha_re.match(c):
                if len(query[idx]) > 0:
                    query.append('')
                    idx += 1
                s += c
            else:
                if len(s) > 0:
                    query[idx] += s
                    s = ''
                    query.append('')
                    idx += 1
                query[idx] += c
        if len(s) > 0:
            query[idx] += s
            s = ''

        for i in range(len(query)):
            query[i] = query[i].upper()

        #kws.eprint(query)


        search = []
        oov_pos = {}
        oov = ''
        for idx, q in enumerate(query):
            while len(q) > 0:
                if self.alpha_re.match(q) and (q not in self.lex):
                    oov += q + '\n'
                    oov_pos[q] = idx
                    search.append('')
                    q = ''
                    continue
                find = False
                for i in range(len(q)):
                    if i == 0:
                        tmp = ''.join(q)
                    else:
                        tmp = ''.join(q[:-i])
                    if tmp in self.lex:
                        find = True
                        search.append(tmp)
                        if i == 0:
                            q = []
                        else:
                            q = q[-i:]
                        break
                if not find:
                    q = q[1:]


        if oov != '':
            p = Popen(['python', './g2p/g2p.py', '--model', './g2p/model/model-6', '-e', 'utf8', '--apply', '-'], stdin=PIPE, stdout=PIPE)
            g2p, _ = p.communicate(oov.encode('utf8'))
            g2p = g2p.decode('utf8').split('\n')[:-1]
            
            for line in g2p:
                line = line.strip().split()
                phone_seq = line[1:]
                seq = ' '.join(phone_seq)
                if seq in self.phone2word:
                    search[oov_pos[line[0]]] = self.phone2word[seq]
                    continue
                
                # sub
                seq = []
                for i in range(len(phone_seq)):
                    seq = phone_seq[0:i]
                    seq.extend(phone_seq[i + 1:])
                    seq = ' '.join(seq)
                    if seq in self.phone2word:
                        search[oov_pos[line[0]]] = self.phone2word[seq]
                        break

                # in
                seq = phone_seq
                for i in range(len(phone_seq) + 1):
                    for j in range(len(self.phone_lst)):
                        tmp = [None] * (len(seq) + 1)
                        tmp[0:i] = seq[0:i]
                        tmp[i] = self.phone_lst[j]
                        tmp[i + 1:] = seq[i:]
                        tmp = ' '.join(tmp)
                        if tmp in self.phone2word:
                            search[oov_pos[line[0]]] = self.phone2word[tmp]
                            break

        tmp_lst = []
        for s in search:
            if s != '':
                tmp_lst.append(s)
        
        search = []
        while len(tmp_lst) > 0:
            s1 = ''.join(tmp_lst)
            s2 = ' '.join(tmp_lst)
            if s1 in self.result_lst:
                search.append(s1)
                break
            elif s2 in self.result_lst:
                search.append(s2)
                break
            else:
                search.append(tmp_lst[0])
            tmp_lst = tmp_lst[1:]

        #kws.eprint(search)


        rerank_dir = './lecture/data/result/'

        penalty = 5

        # rerank result
        rerank_subdict = []
        for i, q in enumerate(search):
            rerank_subdict.append({})
            with open(rerank_dir + q, 'r') as fin:
                for line in fin:
                    line = line.strip().split()[-4:]
                    line[3] = float(line[3])
                    
                    if line[0] in rerank_subdict[i]:
                        lst = rerank_subdict[i][line[0]]
                        if line[3] < lst[3]:
                            rerank_subdict[i][line[0]] = line
                    else:
                        rerank_subdict[i][line[0]] = line

        rerank_dict = {}
        which_dict = {}
        for i in range(len(search)):
            for item in rerank_subdict[i].items():
                if item[0] in rerank_dict:
                    rerank_dict[item[0]][3] = rerank_dict[item[0]][3] - (penalty - 1) + item[1][3]
                else:
                    rerank_dict[item[0]] = copy.deepcopy(item[1])
                    rerank_dict[item[0]][3] += penalty * (len(search) - 1)
                    which_dict[item[0]] = i

                if item[1][1] == rerank_dict[item[0]][2]:
                    rerank_dict[item[0]][3] -= 1
                    rerank_dict[item[0]][2] = copy.deepcopy(item[1][2])
                else:
                    if item[1][3] < rerank_subdict[which_dict[item[0]]][item[0]][3]:
                        rerank_dict[item[0]][1:3] = copy.deepcopy(item[1][1:3])
                        which_dict[item[0]] = i


        output = []
        for _, lst in rerank_dict.items():
            output.append(lst)

        output = sorted(output, key=lambda x: x[3])

        #kws.eprint(len(output))
        output_lst = []
        for lst in output:
            output_lst.append('{} {} {}'.format(lst[0], self.uttid2time[lst[0]], self.uttid2text[lst[0]]))
        
        return output_lst
