(define double-and-print (x) (print (+ x x)))
(define exponent (base exp) (if (= exp 0) 1 (* base (exponent base (- exp 1)))))
(define log-base (base x) (if (= x 1) 0 (+ 1 (log-base base (/ x base)))))
(define factorial (x) (if (= x 0) 1 (* x (factorial (- x 1)))))
(define combination (n k) ( / (factorial n) (* (factorial k) (factorial (- n k)))))
(double-and-print 5)
(double-and-print 10)
(exponent 2 3)
(exponent 3 2)
(exponent 4 0)
(exponent 5 5)
(log-base 2 16)
(log-base 2 256)
(log-base 2 4096)
(log-base 10 100)
(factorial 5)
(combination 5 1)
(combination 5 3)
(combination 5 4)
quit