#!/bin/bash
nosetests --with-cov --cover-html --cov-report html
firefox htmlcov/index.html
