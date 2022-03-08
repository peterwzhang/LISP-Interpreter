(set x 0)
(while (< x 10) (begin (set x (+ x 1)) (set x (+ x 1))))
x
(set x 0)
(while (= x 0) (set x 4))
x
(set x 0)
(while (< x 100) (begin (set x (+ x 1)) (set x (* x 2)) (set x (- x 1))))
x
(set x 0)
(while (< x 1000) (begin (set x (+ x (- 2 1))) (set x (* x (+ 3 2))) (set x (+ x (- 1 2)))))
x
quit