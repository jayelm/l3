#!/usr/bin/env python2

import models
from models import TransducerModel
from tasks import regex2

import gflags
import os
import sys

FLAGS = gflags.FLAGS
gflags.DEFINE_boolean("train", False, "do a training run")
gflags.DEFINE_boolean("test", False, "do a testing run")
gflags.DEFINE_boolean("vis", False, "generate visualization output")
gflags.DEFINE_integer("n_epochs", 0, "number of epochs to run for")
gflags.DEFINE_integer("n_batch", 100, "batch size")
models._set_flags()

def main():
    task = regex2.RegexTask()
    model = TransducerModel(task)

    if FLAGS.train:
        for i_epoch in range(FLAGS.n_epochs):
            e_loss = 0.
            for i_batch in range(100):
                batch = task.sample_train(FLAGS.n_batch)
                b_loss = model.train(batch)
                e_loss += b_loss

            batch = task.sample_train(FLAGS.n_batch)
            e_acc = model.predict(batch)
            print("[loss]    %01.4f" % e_loss)
            print("[trn_acc] %01.4f" % e_acc)

            v_batch = task.sample_val()
            e_v_acc = model.predict(v_batch)
            print("[val_acc] %01.4f" % e_v_acc)
            print("")

            if i_epoch % 10 == 0:
                model.save()

    if FLAGS.test:
        v_batch = task.sample_val()
        e_v_acc = model.predict(v_batch)

        t_batch = task.sample_test()
        e_t_acc = model.predict(t_batch)

        print("[FINAL val_acc] %01.4f" % e_v_acc)
        print("[FINAL tst_acc] %01.4f" % e_t_acc)

    if FLAGS.vis:
        v_batch = task.sample_val()
        preds, labels, hyps = model.predict(v_batch, debug=True)
        for i in range(10):
            task.visualize(v_batch[i], hyps[i], preds[i][0])

if __name__ == "__main__":
    argv = FLAGS(sys.argv)
    main()
