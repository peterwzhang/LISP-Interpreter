(set x 5)
(set y 7)
(begin (set x (* x 2)) (set y (+ x y)))
(print y)
(if (< x y) (begin (print 'Hello) (print 'My) (print 'Name) (print 'is) (print 'Peter)) 1)
quit