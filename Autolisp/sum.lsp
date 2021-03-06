(defun C:HELLO () (princ "Hello world. \n") (princ))

(defun C:sum100()
    (setq test 1 s 0)
    (while (<= test 100)
        (setq s (+ s test))   
        (setq test (1+ test))
    )
    (princ s)
    (princ)
)

(defun sum(arg1)
    (setq test 1 s 0)
    (while (<= test arg1)
        (setq s (+ s test))   
        (setq test (1+ test))
    )
    (princ s)
    (princ)
)

(defun square()
    (command "_line" "0,0" "100,0" "")
    (command "_line" '(100 0) '(100 100) "")
    (command "_line" (list 100 100) (list 0 100) "")
    (command "_line" '(0 100) '(0 0) "")
    (alert "The square is drawn.")
    (princ)
)

(defun drawlines(num)
    (setq count 0)
    (setq y 0) 
    (while (< count num)
        (command "_line" (list 0 y) (list 100 y) "")
        (setq y (+ y 10))
        (setq count (1+ count))
    )
    (princ)
)

(defun drawcircle()
  (if (not (tblsearch "LTYPE" "Dashed"))
     (command ".-linetype" "_load" "Dashed" "acad.lin" "")
  )
  
  (command "_circle" "0,0" "1")
  (command "_chprop" (entlast) "" "_c" "1" "_lt" "Dashed" "")
)
