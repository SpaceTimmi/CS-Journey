;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname space-invaders-starter) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/universe)
(require 2htdp/image)

;; Space Invaders


;; Constants:

(define WIDTH  300)
(define HEIGHT 500)

(define INVADER-X-SPEED 1.5)  ;speeds (not velocities) in pixels per tick
(define INVADER-Y-SPEED 1.5)
(define TANK-SPEED 2)
(define MISSILE-SPEED 10)

(define HIT-RANGE 10)

(define INVADE-RATE 100)

(define BACKGROUND (empty-scene WIDTH HEIGHT))

(define INVADER
  (overlay/xy (ellipse 10 15 "outline" "blue")              ;cockpit cover
              -5 6
              (ellipse 20 10 "solid"   "blue")))            ;saucer

(define TANK
  (overlay/xy (overlay (ellipse 28 8 "solid" "black")       ;tread center
                       (ellipse 30 10 "solid" "green"))     ;tread outline
              5 -14
              (above (rectangle 5 10 "solid" "black")       ;gun
                     (rectangle 20 10 "solid" "black"))))   ;main body

(define TANK-HEIGHT/2 (/ (image-height TANK) 2))

(define MISSILE (ellipse 5 15 "solid" "red"))



;; Data Definitions:

(define-struct game (invaders missiles tank))
;; Game is (make-game  (listof Invader) (listof Missile) Tank)
;; interp. the current state of a space invaders game
;;         with the current invaders, missiles and tank position

;; Game constants defined below Missile data definition

#;
(define (fn-for-game s)
  (... (fn-for-loinvader (game-invaders s))
       (fn-for-lom (game-missiles s))
       (fn-for-tank (game-tank s))))



(define-struct tank (x dir))
;; Tank is (make-tank Number Integer[-1, 1])
;; interp. the tank location is x, HEIGHT - TANK-HEIGHT/2 in screen coordinates
;;         the tank moves TANK-SPEED pixels per clock tick left if dir -1, right if dir 1

(define T0 (make-tank (/ WIDTH 2) 1))   ;center going right
(define T1 (make-tank 50 1))            ;going right
(define T2 (make-tank 50 -1))           ;going left

#;
(define (fn-for-tank t)
  (... (tank-x t) (tank-dir t)))



(define-struct invader (x y dx))
;; Invader is (make-invader Number Number Number)
;; interp. the invader is at (x, y) in screen coordinates
;;         the invader along x by dx pixels per clock tick

(define I1 (make-invader 150 100 12))           ;not landed, moving right
(define I2 (make-invader 150 HEIGHT -10))       ;exactly landed, moving left
(define I3 (make-invader 150 (+ HEIGHT 10) 10)) ;> landed, moving right


#;
(define (fn-for-invader invader)
  (... (invader-x invader) (invader-y invader) (invader-dx invader)))


(define-struct missile (x y))
;; Missile is (make-missile Number Number)
;; interp. the missile's location is x y in screen coordinates

(define M1 (make-missile 150 300))                       ;not hit U1
(define M2 (make-missile (invader-x I1) (+ (invader-y I1) 10)))  ;exactly hit U1
(define M3 (make-missile (invader-x I1) (+ (invader-y I1)  5)))  ;> hit U1

#;
(define (fn-for-missile m)
  (... (missile-x m) (missile-y m)))



(define G0 (make-game empty empty T0))
(define G1 (make-game empty empty T1))
(define G2 (make-game (list I1) (list M1) T1))
(define G3 (make-game (list I1 I2) (list M1 M2) T1))

;; =================
;; Functions:
;; Game -> Game
;; start the world with (main G0)
;;

(define (main g)
  (big-bang g             ; Game
    (on-tick update-game) ; Game -> Game
    (to-draw render-game) ; Game -> Image
    (stop-when end-game?) ; Game -> Boolean
    (on-key  move-tank))) ; Game KeyEvent -> Game

;;Game -> Game
;; produce the next position of the missiles, tank and invaders.
;;         and also generate a random position for a new invader.

;; REMOVED ALL THE TESTS FOR Update-Game & Update-Invader because that would involve testing for randomness, which I can't do now.
#;
(check-expect (update-game G1) (make-game empty
                                          empty
                                          (make-tank (+ TANK-SPEED (tank-x T1))
                                                     (tank-dir T1))))
#;
(check-expect (update-game G2) (make-game (list (make-invader (+ (invader-x I1) (invader-dx I1))
                                                              (+ INVADER-Y-SPEED (invader-y I1))
                                                              (+ INVADER-X-SPEED (invader-dx I1))))
                                          (list (make-missile 150
                                                              (- 300 MISSILE-SPEED)))
                                          (make-tank (+ TANK-SPEED (tank-x T1))
                                                     (tank-dir T1))))
#;
(check-expect (update-game G3) (make-game (list (make-invader (+ (invader-x I1) (invader-dx I1))
                                                              (+ INVADER-Y-SPEED (invader-y I1))
                                                              (+ INVADER-X-SPEED (invader-dx I1)))
                                                (make-invader (+ (invader-x I2) (invader-dx I2))
                                                              (+ INVADER-Y-SPEED (invader-y I2))
                                                              (+ INVADER-X-SPEED (invader-dx I2))))
                                          (list (make-missile 150
                                                              (- 300 MISSILE-SPEED))
                                                (make-missile (invader-x I1)
                                                              (- (+ (invader-y I1) 10) MISSILE-SPEED)))
                                          (make-tank (+ TANK-SPEED (tank-x T1))
                                                     (tank-dir T1))))


#;
(define (update-game s) s) ;stub

;; template from Game
(define (update-game s)
  (make-game (update-invaders (game-invaders s)
                              (game-missiles s))
             (update-missiles (game-missiles s))
             (update-tank     (game-tank s))))


;; ListOfInvaders -> ListOfInvaders
;; produce the new coordinates of the invaders on screen.
#;
(check-expect (update-invaders (list I1) empty) (list (make-invader (+ (invader-x I1) (invader-dx I1))
                                                                    (+ INVADER-Y-SPEED (invader-y I1))
                                                                    (+ INVADER-X-SPEED (invader-dx I1)))))
#;
(check-expect (update-invaders (list I1 I2) empty) (list (make-invader (+ (invader-x I1) (invader-dx I1))
                                                                       (+ INVADER-Y-SPEED (invader-y I1))
                                                                       (+ INVADER-X-SPEED (invader-dx I1)))
                                                         (make-invader (+ (invader-x I2) (invader-dx I2))
                                                                       (+ INVADER-Y-SPEED (invader-y I2))
                                                                       (+ INVADER-X-SPEED (invader-dx I2)))))
#;
(define (update-invaders loi lom) loi);stub

;; Adding coverage for updating invader positions
#;
(define (update-invaders loi lom)
  (cond [(empty? loi) (random-invader empty)]
        [else (cons (move-invader (first loi))
                    (update-invaders (rest loi) lom))]))

;; Adding coverage for hits
(define (update-invaders loi lom)
  (cond [(empty? loi) (random-invader empty)]
        [else (if (hit-by-missile? lom (first loi))
                  (update-invaders (rest  loi) lom)
                  (cons (move-invader (first loi))
                        (update-invaders (rest loi) lom)))]))


;; Invader ListOfMissiles -> Boolean
;; given an invader return true if the invader is an invalid invader.
;; invalidity means the invader has been hit by a missile in the list of missiles
(check-expect (hit-by-missile? empty I1)        false)
(check-expect (hit-by-missile? (list M1) I1)    false)
(check-expect (hit-by-missile? (list M2) I1)     true)
(check-expect (hit-by-missile? (list M1 M2) I1)  true)
(check-expect (hit-by-missile? (list M1 M1) I1) false)
#;
(define (hit-by-missile? lom i) false) ;stub

(define (hit-by-missile? lom i)
  (cond [(empty? lom) false]
        [else (if (hit? i (first lom))
                  true
                  (hit-by-missile? (rest lom) i))]))


;; Invader Missile -> Boolean
;; given an invader and a missile return true if the missiles hits the invader
;; hit in this case is if the missile is within the HIT-RANGE of a invader,
;; and if the missile is below the invader.
(check-expect (hit? I1 M1) false)
(check-expect (hit? I1 M2) true)
#;
(define (hit? i m) false) ;stub
#;
(define (hit? i m)
  (and (< (- (missile-y m)
             (invader-y i))
          100)
       (= (missile-x m)
          (invader-x i))))

(define (hit? i m)
  (and (within-range? 0
                      HIT-RANGE
                      (- (missile-y m)
                         (invader-y i)))
       (within-range? (- (invader-x i) (/ (image-width INVADER) 2))
                      (+ (invader-x i) (/ (image-width INVADER) 2))
                      (missile-x m))))


;; List -> List
;; generates a new invader.
(define (random-invader l)
  (if (within-range? 95 100 (random 100))
      (cons (make-invader (random WIDTH)
                          (/ (image-height INVADER) 2)
                          -12) empty)
      empty))
#;
(define (random-invader e)
  (cons (make-invader (random WIDTH)
                      (/ (image-height INVADER) 2)
                      -12)
        empty))
;; Number Number Number -> Boolean
;; given three numbers sm, lg and n; check if n is within the boundary sm and lg (inclusive of both sm and lg).
;; CRITERIA: lg > sm 
(define (within-range? sm lg n)
  (and (<= sm n)
       (>= lg n)))



;; Invader -> Invader
;; given a single invader update its coordinate on screen.
#;
(check-expect (move-invader I1) (make-invader (+ (invader-x I1) (invader-dx I1))
                                              (+ INVADER-Y-SPEED (invader-y I1))
                                              (+ INVADER-X-SPEED (invader-dx I1))))
;; Add more test coverage

;; template from invaders
(define (move-invader i)
  (cond [(> (+ (invader-x i) (/ (image-width INVADER) 2)) WIDTH)
         (make-invader (- WIDTH (/ (image-width INVADER) 2))
                       (+ INVADER-Y-SPEED
                          (invader-y i))
                       (- (invader-dx i)))] ;; Hits right wall
        [(< (invader-x i) (/ (image-width INVADER) 2))
         (make-invader (/ (image-width INVADER) 2) 
                       (+ INVADER-Y-SPEED
                          (invader-y i))
                       (- (invader-dx i)))] ;; Hits left wall
        [else (make-invader (+ (invader-x i)
                               (invader-dx i))
                            (+ INVADER-Y-SPEED
                               (invader-y i))
                            ;(+ INVADER-X-SPEED
                            (invader-dx i))])) ;; Move invader as usual


;; ListOfMissiles -> ListOfMissiles
;; produce the new coordinates of the missiles on screen.
(check-expect (update-missiles empty) empty)
(check-expect (update-missiles (list M1)) (list (make-missile 150
                                                              (- 300 MISSILE-SPEED))))
(check-expect (update-missiles (list M1 M2)) (list (make-missile 150
                                                                 (- 300 MISSILE-SPEED))
                                                   (make-missile (invader-x I1)
                                                                 (- (+ (invader-y I1) 10) MISSILE-SPEED))))
#;
(define (update-missiles lom) lom) ;stub
#;
(define (update-missiles lom)
  (cond [(empty? lom) empty]
        [else
         (cons (move-missile (first lom))
               (update-missiles (rest lom)))]))

;; remove missiles that exceed the boundary.
(define (update-missiles lom)
  (cond [(empty? lom) empty]
        [else
         (if (left-boundary? (first lom))
             (update-missiles (rest lom))
             (cons (move-missile (first lom))
                   (update-missiles (rest lom))))]))


;; Missile -> Boolean
;; return true if a missile has left the screen, return false otherwise.
(check-expect (left-boundary? M1) false)
(check-expect (left-boundary? (make-missile 10 -10)) true)
#;
(define (left-boundary? m) false) ;stub

(define (left-boundary? m)
  (< (missile-y m) 1))


;; Missile -> Missile
;; update the coordinate of a given missile.
(check-expect (move-missile M1) (make-missile 150 (- 300 MISSILE-SPEED)))

;; template copied from Missile
(define (move-missile m)
  (make-missile (missile-x m)
                (- (missile-y m) MISSILE-SPEED)))



;; Tank -> Tank
;; produce the new coordinates for the tank.
;; Tank should stay at the end of the screen so as not to exceed WIDTH boundary
(check-expect (update-tank T0) (make-tank (+ (* (tank-dir T0)
                                                TANK-SPEED)
                                             (tank-x T0))
                                          (tank-dir T0)))
(check-expect (update-tank T2) (make-tank (+ (* (tank-dir T2)
                                                TANK-SPEED)
                                             (tank-x T2))
                                          (tank-dir T2)))
(check-expect (update-tank (make-tank (+ (- WIDTH) (/ (image-width TANK) 2)) -1)) (make-tank (/ (image-width TANK) 2) -1)) ; exceed left
(check-expect (update-tank (make-tank (+ WIDTH (image-width TANK))  1)) (make-tank (- WIDTH (/ (image-width TANK) 2)) 1)); exceed right

#;
(define (update-tank t) t) ;stub

(define (update-tank t)
  (cond [(< (tank-x t) (/ (image-width TANK) 2))
         (make-tank (/ (image-width TANK) 2)
                    (tank-dir t))] ;; TANK trying to exceed left
        [(> (tank-x t) (- WIDTH (/ (image-width TANK) 2)))
         (make-tank (- WIDTH (/ (image-width TANK) 2))
                    (tank-dir t))] ;; TANK trying to exceed right
        [else (make-tank (+ (* (tank-dir t) TANK-SPEED)
                            (tank-x t))
                         (tank-dir t))]))



;; Game -> Image
;; render tank, invaders and missiles on the BACKGROUND.
(check-expect (render-game G0) (place-image TANK
                                            (tank-x T0)
                                            (- HEIGHT TANK-HEIGHT/2)
                                            BACKGROUND))

(check-expect (render-game G2) (place-image INVADER
                                            (invader-x I1)
                                            (invader-y I1)
                                            (place-image MISSILE
                                                         (missile-x M1)
                                                         (missile-y M1)
                                                         (place-image TANK
                                                                      (tank-x T1)
                                                                      (- HEIGHT TANK-HEIGHT/2)
                                                                      BACKGROUND))))

#;
(define (render-game s) BACKGROUND) ;stub


(define (render-game s)
  (render-invaders (game-invaders s)
                   (game-missiles s)
                   (game-tank s)))


;; ListOfInvaders ListOfMissiles Tank -> Image
;; takes the list of invaders, renders them and then calls render-missile.
;; render-game check-expects will test this function

(define (render-invaders loi lom t)
  (cond [(empty? loi) (render-missiles lom t)]
        [else (place-image INVADER
                           (invader-x (first loi))
                           (invader-y (first loi))
                           (render-invaders (rest loi)
                                            lom t))]))

;; ListOfMissiles Tank -> Image
;; takes the list of missiles, renders them and calls render tank
;; render-game check-expects will test this function
(define (render-missiles lom t)
  (cond [(empty? lom) (render-tank t)]
        [else (place-image MISSILE
                           (missile-x (first lom))
                           (missile-y (first lom))
                           (render-missiles (rest lom) t))]))

;; Tank -> Image
;; takes a tank struct and renders it on BACKGROUND
;; render-game check-expects will test this function

;; template from TANK
(define (render-tank t)
  (place-image TANK
               (tank-x t)
               (- HEIGHT TANK-HEIGHT/2)
               BACKGROUND))
  
                                            
;; Game -> Boolean
;; stop when any invaders hits the bottom of the screen
(check-expect (end-game? G0) false)
(check-expect (end-game? G1) false)
(check-expect (end-game? G2) false)
(check-expect (end-game? (make-game (list I1 I3)
                                    empty
                                    T1)) true)
#;
(define (end-game? s) false) ;stub

(define (end-game? s)
  (invader-hit-floor (game-invaders s)))


;; Loi -> Boolean
;; return true if any invader in the list has a y coordinate greater than HEIGHT
;; else return false otherwise
(check-expect (invader-hit-floor empty)        false)
(check-expect (invader-hit-floor (list I1))    false)
(check-expect (invader-hit-floor (list I3))     true)
(check-expect (invader-hit-floor (list I1 I2)) false)
(check-expect (invader-hit-floor (list I1 I3))  true)


(define (invader-hit-floor loi)
  (cond [(empty? loi) false]
        [else (if (past-landing? (first loi))
                  true
                  (invader-hit-floor (rest loi)))]))


;; Invader -> Boolean
;; return true the given invader has landed (y coordinate greater than HEIGHT of BACKGROUND)
;; else return false otherwise
(check-expect (past-landing? I1) false)
(check-expect (past-landing? I2) false)
(check-expect (past-landing? I3) true)

(define (past-landing? i)
  (> (invader-y i) HEIGHT))

;; Game KeyEvent -> Game
;; if the right arrow key is pressed (and tank was going  left) move tank right
;; if the  left arrow key is pressed (and tank was going rigth) move tank left
;; else maintain same direction
(check-expect (move-tank (make-game empty empty T1)     "a") (make-game empty empty T1))
(check-expect (move-tank (make-game empty empty T1) "right") (make-game empty empty T1))
(check-expect (move-tank (make-game empty empty T1)  "left") (make-game empty empty (make-tank (tank-x T1) -1)))
(check-expect (move-tank (make-game empty empty T2)     "a") (make-game empty empty T2))
(check-expect (move-tank (make-game empty empty T2) "right") (make-game empty empty (make-tank (tank-x T2)  1)))
(check-expect (move-tank (make-game empty empty T2)  "left") (make-game empty empty T2))
(check-expect (move-tank (make-game empty empty T1)     " ") (make-game empty (list (make-missile (tank-x T1) (- HEIGHT (image-height TANK)))) T1))
(check-expect (move-tank (make-game empty empty T2)     " ") (make-game empty (list (make-missile (tank-x T2) (- HEIGHT (image-height TANK)))) T2))


(define (move-tank g ke)
  (cond [(and (key=? ke "right")
              (= (tank-dir (game-tank g)) -1)) ;; tank was moving left and right was pressed.
         (make-game (game-invaders g)
                    (game-missiles g)
                    (change-dir (game-tank g)))]
        [(and (key=? ke "left")
              (= (tank-dir (game-tank g))  1)) ;; tank was moving right and left was pressed.
         (make-game (game-invaders g)
                    (game-missiles g)
                    (change-dir (game-tank g)))]
        [(key=? ke " ")
         (make-game (game-invaders g)
                    (add-missile (game-tank g) (game-missiles g))
                    (game-tank g))]
        [else g]))

;; Number Tank -> Tank
;; change the direction of a given tank
(define (change-dir t)
  (make-tank (tank-x t)
             (- (tank-dir t))))

;; Tank ListOfMissiles -> ListOfMissiles
;; given a tank and list of missiles, add a new missile with the x and y coordinate being just above the tank.

(define (add-missile t lom)
  (cons (make-missile (tank-x t)
                      (- HEIGHT (image-height TANK)))
        lom))



;; START GAME
(main G0)