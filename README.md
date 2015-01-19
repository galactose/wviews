Wviews [![Build Status](https://travis-ci.org/galactose/wviews.svg?branch=master)](https://travis-ci.org/galactose/wviews)
=======
Wviews is an artificial intelligence system extension for generating world view answer sets for epistemic logic programs.

This software implements the theory in the 1994 paper "*Logic programming and reasoning with incomplete information*" by Michael Gelfond in the Journal the Annals of Mathematics and Artificial Intelligence and the 2007 paper "*Epistemic Reasoning in Logic Programs*" by Yan Zhang in the International Joint Conferences on Artificial Intelligence. 

Epistemic logic programs extend disjunctive logic programs by allowing new modal operators K and M, where set of rules T and for formula F, KF represents "*F is known by a reasoner to be true given rules T*" and MF represents "*F is believed true given rules T*". This extension provides a richer semantics that allows representation of knowledge in the light of unknown information or inconsistent knowledge.

Wviews accepts rules of the form

    A1 v ... v An :- K/MB1, ... K/MBn, ..., C1, ... Cn, not D1, ..., not Dn.

where A, B, C and D are logically atomic.

Example
=======

The following epistemic logic program represents the procedure for deciding if a student is eligible of a scholarship.

    eligible(alice) :- highGPA(alice).
    eligible(alice) :- minority(alice), fairGPA(alice).
    ~eligible(alice) :- ~fairGPA(alice), ~highGPA(alice).
    interview(alice) :- ~Keligible(alice), ~K~eligible(alice).
    fairGPA(alice) v highGPA(alice).

If student Alice has a high GPA, they are eligible. If Alice is a minority and has a fair GPA, Alice is also eligible. If Alice has neither a fair or high GPA, she is ineligible for consideration. Finally if we do not know whether Alice is eligible or ineligible, interview Alice to determine. We also add that it is the case that Alice has a fair GPA or a high GPA.

This program yields the world view

    WV = {{highGPA(alice), eligible(alice), interview(alice)}, {fairGPA(alice), interview(alice)}}

This indicates that given the unknown status of alices eligibility, interview her in either case, but in the case that she has a high GPA she is eligible.

Prerequisites
=======
Wviews requires the disjunctive logic program tool DLV. DLV can be downloaded at http://www.dlvsystem.com/dlv/.

Authors
=======
Wviews was created by [Michael Kelly](https://github.com/galactose) for consideration of an honours degree in Computer Science. This was under the supervision of Professor Yan Zhang www.scm.uws.edu.au/~yan at the University of Western Sydney.
