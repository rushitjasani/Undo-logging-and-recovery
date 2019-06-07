#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

transactions = dict()
variables_disk = dict()
variables_memory = dict()
len_of_trans = dict()
order_of_trans = []
done_dict = dict()
temp_var_map = dict()
temp_var = dict()

inpFile = sys.argv[1]
x = int(sys.argv[2])
output_file = open('2018201034_1.txt', 'w')


def operate(a, b, op):
    if op is '+':
        return a + b
    if op is '-':
        return a - b
    if op is '*':
        return a * b
    if op is '/':
        return float(a) / float(b)


def print_values_in_memory():
    s = ''
    for i in sorted(variables_memory):
        s += i + ' ' + str(variables_memory[i]) + ' '
    s = s[:-1]
    output_file.writelines(s + '\n')


def print_values_in_disk():
    s = ''
    for i in sorted(variables_disk):
        s += i + ' ' + str(variables_disk[i]) + ' '
    s = s[:-1]
    output_file.write(s + '\n')


def find_op(line):
    if '+' in line:
        return '+'
    elif '-' in line:
        return '-'
    elif '*' in line:
        return '*'
    elif '/' in line:
        return '/'


def perform_log(cur_transaction, x, start_pos):
    if len_of_trans[cur_transaction] <= start_pos:
        done_dict[cur_transaction] = True
        return
    instructions = transactions[cur_transaction]
    instructions = instructions[start_pos:start_pos + x]

    if 0 == start_pos:
        output_file.write('<START ' + cur_transaction + '>' + '\n')
        print_values_in_memory()
        print_values_in_disk()

    for line in instructions:
        line = line.strip()
        line = line.replace(' ', '')
        if line.split('(')[0] == 'READ':
            var = line[line.find('(') + 1:line.find(',')]
            value = line[line.find(',') + 1:line.find(')')]

            if var not in temp_var_map.keys():
                temp_var_map[var] = value
                temp_var[value] = variables_disk[var]
                variables_memory[var] = variables_disk[var]
            else:
                temp_var[value] = variables_memory[var]
                temp_var_map[var] = value
        elif 'WRITE' == line.split('(')[0]:
            var = line[line.find('(') + 1:line.find(',')]
            value = line[line.find(',') + 1:line.find(')')]
            output_file.write('<' + cur_transaction + ', ' + var + ', '
                              + str(variables_memory[var]) + '>' + '\n')
            variables_memory[var] = int(temp_var[value])
            print_values_in_memory()
            print_values_in_disk()
        elif line.split('(')[0] == 'OUTPUT':

            var = line[line.find('(') + 1:line.find(')')]
            variables_disk[var] = variables_memory[var]
        else:
            var1 = line[0:line.find(':')]
            op = find_op(line)
            var2 = line[line.find('=') + 1:line.find(op)]
            val = line[line.find(op) + 1:]
            temp_var[var1] = operate(temp_var[var2], int(val), op)

    if len_of_trans[cur_transaction] <= start_pos + x:
        output_file.write('<COMMIT ' + cur_transaction + '>' + '\n')
        print_values_in_memory()
        print_values_in_disk()


def operate_1(a, b, op):
    if op is '+':
        return a + b
    if op is '-':
        return a - b
    if op is '*':
        return a * b
    if op is '/':
        return float(a) / float(b)


def undo_logs(x):
    i = 0
    cur_transaction = order_of_trans[i]
    start_pos = 0
    while True:
        perform_log(cur_transaction, x, start_pos)
        i += 1
        if i % len(transactions) == 0:
            start_pos += x
            i = 0
        cur_transaction = order_of_trans[i]
        false_count = list()
        for (key, val) in done_dict.iteritems():
            if val == False:
                false_count.append('FALSE')
        if len(false_count) == 0:
            break


def read_file(inpFile):
    val = False
    transaction_no = None
    for line in open(inpFile):
        if val == False:
            variables = line.split()
            ll = range(len(variables))
            for i in ll:
                if 0 == i % 2:
                    variables_disk[variables[i]] = int(variables[i + 1])
            val = True
        elif line.split(' ')[0][0] == 'T':
            ls = line.split(' ')
            transaction_no = ls[0]
            order_of_trans.append(transaction_no)
            len_of_trans[transaction_no] = int(ls[1])
            transactions[transaction_no] = list()
        elif line.find('(') == True:
            transactions[transaction_no] += [line[:-1]]
        elif not line.strip():
            transaction_no = None
        else:
            transactions[transaction_no] += [line[:-1]]

    for i in transactions.keys():
        done_dict[i] = False


read_file(inpFile)
undo_logs(x)
output_file.close()
