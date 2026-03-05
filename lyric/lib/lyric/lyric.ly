# Lyric Standard Library
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.
importpy os
importpy time
importpy math
importpy glob
importpy random
importpy datetime

# sleep for x seconds, can be 0.1
def sleep(var seconds) {
    time.sleep(seconds)
}

# return random between 0.0 and 1.0
flt randflt() {
    return random.random()
}

# return random integer between low and high
int randint(int low, int high) {
    return random.randint(low, high)
}

# return a random array element
var randarr(arr list) {
    return random.choice(list)
}

# seed the random
def seed(int value) {
    random.seed(value)
}

# change directory
var cd(str path) {
    os.chdir(path)
}

# list directory
arr ls(str lspath) {
    if os.path.isdir(lspath)
        return os.listdir(lspath)
    else
        return glob.glob(lspath)
    end
}

# make directory
def mkdir(str path) {
    os.mkdir(path)
}

# print working directory
str pwd() {
    return os.getcwd()
}

# get environment variable
str env(str name) {
    return os.getenv(name)
}

# set environment variable
def set(str name, str value) {
    os.environ[name] = value
}

# get pid
int pid() {
    return os.getpid()
}

# check if file exists
god exists(str path) {
    return os.path.exists(path)
}

# check if is file
god isfile(str path) {
    return os.path.isfile(path)
}

# check if is directory
god isdir(str path) {
    return os.path.isdir(path)
}

# remove file
def rm(str path) {
    os.remove(path)
}

# remove dir
def rmdir(str path) {
    os.rmdir(path)
}

# return the (date, time)
tup date() {
    now = datetime.datetime.now()
    return (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
}

# return format string date
str datefmt(str fmt) {
    now = datetime.datetime.now()
    return now.strftime(fmt)
}

# return unix time
int now() {
    return math.floor(time.time())
}

# returns joined path
str join(str path, str file) {
    return os.path.join(path, file)
}

# returns full path
str path(str file) {
    return os.path.abspath(file)
}

# returns basename
str base(str file) {
    return os.path.basename(file)
}

# returns dirname
str dir(str file) {
    return os.path.dirname(file)
}


