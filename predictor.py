import classifiers, argparse, itertools, sys, random
from sklearn.metrics import classification_report, precision_recall_fscore_support

def kfolds(input, output, classifier, verbose=False, num_folds=10):
    if num_folds < 2:
        num_folds = 2
        print "Defaulting to 2-folds at minimum..."

    if verbose:
        print "Running k-folds Cross Validation..."
        print "Data separated into %d-folds..." % (num_folds)
        print "-------------------BEGIN TESTING------------------"

    train_errors = []
    test_errors = []
    accuracies = []
    p_overall = []
    p_neutral = []
    p_sarcastic = []
    r_overall = []
    r_neutral = []
    r_sarcastic = []
    f1_overall = []
    f1_neutral = []
    f1_sarcastic = []

    fold_size = len(input)/num_folds
    if fold_size < 1:
        fold_size = 1
        num_folds = len(input)
        print "Fold size too small. Defaulting to fold size of one (%d-folds)" % (num_folds)

    for i in xrange(num_folds):
        trainX = input[0: fold_size*i] + input[fold_size*(i+1):]
        trainY = output[0: fold_size*i] + output[fold_size*(i+1):]
        # TODO: shuffle data?
        testX = input[fold_size*i: fold_size*(i+1)]
        testY = output[fold_size*i: fold_size*(i+1)]

        classifier.train(trainX, trainY)

        trainPredY = classifier.predict(trainX)
        testPredY = classifier.predict(testX)
        accuracy = accuracy_score(testY, testPredY)
        p, r, f1, s = precision_recall_fscore_support(testY, testPredY,
                                                  labels=None,
                                                  average=None,
                                                  sample_weight=None)

        accuracies.append(accuracy)

        p_overall.append(sum(p)/float(len(p)))
        r_overall.append(sum(r)/float(len(r)))
        f1_overall.append(sum(f1)/float(len(f1)))

        #NOTE: Gathering neutral and sarcastic stats like this does not work
        #      if one of them is absent in the test set
        p_neutral.append(p[0])
        r_neutral.append(r[0])
        f1_neutral.append(f1[0])

        p_sarcastic.append(p[1])
        r_sarcastic.append(r[1])
        f1_sarcastic.append(f1[1])

        if verbose:
            # Hack due to the way classification report uses target names
            target_names = []
            if 0 in testY:
                target_names.append("neutral")
            if 1 in testY:
                target_names.append("sarcastic")

            print "Fold #%d:" % (i+1)
            print('Accuracy: %0.03f' % accuracy)
            print(classification_report(testY, testPredY, target_names=target_names, digits=3))
    
    if verbose:
        print "-------------------END TESTING--------------------"
        print ""
        print "AVERAGES ACROSS FOLDS:"
        print "" 
        print "Accuracy: %0.03f" % (sum(accuracies)/float(len(accuracies)))
        print "{0:12s} {1:12s} {2:7s} {3:12s}".format("", "precision", "recall", "f1-score")
        print ""
        fmt = "{0:12s} {1:9.2f} {2:9.2f} {3:9.2f}"
        print fmt.format("neutral",
                        sum(p_neutral)/float(len(p_neutral)),
                        sum(r_neutral)/float(len(r_neutral)),
                        sum(f1_neutral)/float(len(f1_neutral)))
        print fmt.format("sarcastic",
                        sum(p_sarcastic)/float(len(p_sarcastic)),
                        sum(r_sarcastic)/float(len(r_sarcastic)),
                        sum(f1_sarcastic)/float(len(f1_sarcastic)))
        print ""
        print fmt.format("avg / total",
                        sum(p_overall)/float(len(p_overall)),
                        sum(r_overall)/float(len(r_overall)),
                        sum(f1_overall)/float(len(f1_overall)))

VERBOSE = False
def main():
    global VERBOSE, NUM_PROB
    parser = argparse.ArgumentParser(description='Runs a sarcasm classifier on tweets.')
    parser.add_argument("-c", action="store", help="which classifier to use", type=str, default=None)
    parser.add_argument("-v", action="store_true", help="verbose output", default=False)
    parser.add_argument("-f", action="store", help="how many folds to use", type=int, default=10)
    args = parser.parse_args()

    # TODO: read_files
    input = ["ga", "fas", "Asdf", "asdf"]
    output = [1, 0, 1, 0]


    if args.v:
        VERBOSE = True

    if args.c is None:
        print "Defaulting to Baseline..."
        classifier = classifiers.Baseline()        
    elif args.c == "Baseline":
        classifier = classifiers.Baseline()
    else:
        raise Exception("Did not recognize the desired classifier.")

    kfolds(input, output, classifier, True, args.f)

if __name__ == "__main__":
    main()
