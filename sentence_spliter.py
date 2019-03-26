# -*- coding: utf-8 -*-

import os.path
import re
from io import open

import loading_data
import utils
from feature.feature import Feature
from regex import Regex


class SentenceSpliter():
    def __init__(self, path="models/modelRF.dump", is_training=False):
        self.classifier = None
        self.feature_model = None
        self.regex_rule = Regex()
        self.c_dir = os.path.abspath(os.path.dirname(__file__))
        print self.c_dir
        self.model_path = "%s/%s" % (self.c_dir, path)
        if not is_training:
            if os.path.exists(self.model_path) and not is_training:
                model = utils.pickle_load(self.model_path)
                self.classifier = model.classifier
                self.feature_model = model.feature_model
            else:
                print "Unable to load the spliter model. %s" % path
                exit(-1)

    def make_feature(self, file=None):
        self.feature_model = Feature()
        if file is None:
            file = loading_data.load_data_train("data/train.dat")
            file = self.regex_rule.run_regex_training(file)
            features_list, label_list = self.feature_model.gen_feature_matrix(file)
            sens = file.split('\n')
            for sen in sens:
                a, b = self.feature_model.gen_feature_matrix(sen)
                features_list += a
                label_list += b
        else:
            features_list, label_list = self.feature_model.gen_feature_matrix(file)
        return features_list, label_list

    def split_paragraph(self, par):
        sens = []
        try:
            paragraph = par
            par, number, url, url2, email, datetime, non_vnese, mark, mark3, mark4 = \
                self.regex_rule.run_regex_predict(par)
            features, _ = self.make_feature(par)
            if not features:
                sens.append(paragraph.strip())
                return sens
            labels = self.classifier.predict(features)
            idx = 0
            pos_start = 0
            pos_end = 0
            for c in par:
                if Feature.is_splitter_candidate(c):
                    if idx < len(labels) and labels[idx] == 1:
                        sens.append(par[pos_start:pos_end + 1].strip())
                        pos_start = pos_end + 1
                    idx += 1
                pos_end += 1
            if pos_start < len(par):
                sens.append(par[pos_start:].strip())
            par = '\n'.join(sens)
            par = self.regex_rule.restore_info(par, number, url, url2, email, datetime, non_vnese, mark, \
                                               mark3, mark4)
            sens = par.split('\n')
        except:
            False
        return sens

    def split(self, pars):
        pars = pars.replace(u'\r', u'\n')
        pars = re.compile(u'\n+').sub(u'\n', pars)
        pars = pars.split('\n')
        sens = []
        for par in pars:
            if par.strip():
                s = self.split_paragraph(par)
                sens += s
        return sens


def train():
    sentence_spliter = SentenceSpliter(is_training=True)
    sentence_spliter.train()


def demo_cml():
    sentence_spliter = SentenceSpliter()
    while True:
        par = raw_input("Enter paragraph: ")
        try:
            par = unicode(par)
        except:
            par = unicode(par, encoding="UTF-8")
        print "\nParagraph: ", par
        if len(par) < 2:
            continue
        print "--------------------------------"
        print "Result:"
        list_sens = sentence_spliter.split(par)
        idx = 0
        for sen in list_sens:
            print u"{} :{}".format(idx, sen)
            idx += 1


def demo_file():
    sentence_spliter = SentenceSpliter()
    while True:
        path = raw_input("File: ")
        f = open(path, encoding="UTF-8")
        doc = ''.join(f.readlines())
        f.close()
        list_sens = sentence_spliter.split(doc)
        idx = 0
        for sen in list_sens:
            print(u"{} :{}".format(idx, sen))
            idx += 1


if __name__ == "__main__":
    demo_file()
    # demo_cml()
