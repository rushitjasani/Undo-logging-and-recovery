#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

variables_disk = dict()
logs = list()
start_ckpt_line_no = -1
end_ckpt_line_no = -1
input_file = sys.argv[1]
output_file = open('2018201034_2.txt', 'w')


def undo_all():
    global logs
    l = logs[::-1]
    commited = list()
    for line in l:
        if line[0] == 'T':
            s = line.replace(' ', '').split(',')
            if s[0] not in commited:
                variables_disk[s[1]] = int(s[2])
        elif line.split(' ')[0] == 'COMMIT':
            commited.append(line.split(' ')[1])


def undo_only_start_present():
    global logs
    l = logs[start_ckpt_line_no]
    ts = l[l.find('(') + 1:l.find(')')].replace(' ', '').replace(',',
            ' ')
    trans_active_at_ckpt = ts.split(' ')

    commited = list()
    for line in logs[::-1]:
        if len(trans_active_at_ckpt) == 0:
            break
        if line[0] == 'T':
            s = line.replace(' ', '').split(',')
            if s[0] not in commited:
                variables_disk[s[1]] = int(s[2])
        elif line.split(' ')[0] == 'COMMIT':
            commited.append(line.split(' ')[1])
        elif line.split(' ')[0] == 'START':
            ls = line.split(' ')
            if ls[1] != 'CKPT':
                if ls[1] in trans_active_at_ckpt:
                    trans_active_at_ckpt.remove(ls[1])


def undo_end_present():
    commited = list()
    global logs
    l = logs[start_ckpt_line_no + 1:]
    for line in l[::-1]:
        if line[0] == 'T':
            s = line.replace(' ', '').split(',')
            if s[0] not in commited:
                variables_disk[s[1]] = int(s[2])
        elif line.split(' ')[0] == 'COMMIT':
            commited.append(line.split(' ')[1])


def do_recovery():
    global start_ckpt_line_no
    global end_ckpt_line_no

    if end_ckpt_line_no < start_ckpt_line_no:
        end_ckpt_line_no = -1

    if start_ckpt_line_no == -1 and end_ckpt_line_no == -1:
        undo_all()
    elif -1 == end_ckpt_line_no and start_ckpt_line_no != -1:
        undo_only_start_present()
    elif start_ckpt_line_no == -1 and end_ckpt_line_no != -1:
        err = 'end ckpt found without start ckpt'
        print err
    elif start_ckpt_line_no != -1 and end_ckpt_line_no != -1:
        undo_end_present()
    else:
        pass


def read_file(input_file):
    global start_ckpt_line_no
    global end_ckpt_line_no
    line_no = 1
    transaction_no = None
    for line in open(input_file):
        if line_no == 1:
            variables = line.split()
            for i in xrange(len(variables)):
                if i % 2 == 0:
                    variables_disk[variables[i]] = int(variables[i + 1])
        else:
            if line.strip():
                logs.append(line[1:-2])
                if line.find('START') != -1 and line.find('CKPT') != -1:
                    start_ckpt_line_no = line_no - 3

                if line.find('END') != -1 and line.find('CKPT') != -1:
                    end_ckpt_line_no = line_no - 3
        line_no += 1


def write_output():
    s = ''
    for i in sorted(variables_disk):
        s += i + ' ' + str(variables_disk[i]) + ' '
    s = s[:-1]
    output_file.write(s + '\n')


read_file(input_file)
do_recovery()

write_output()
output_file.close()
