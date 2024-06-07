# files:
remove a file: 		`rm -f <FILE_NAME>`
<br>
remove a folder: 	`rm -r <DIRECTORY_NAME>`
<br>
rename a file: 		`mv <OLD_FILE_NAME> <NEW_FILE_NAME>`
<br>
copy a file: 		`cp <OLD/FILE/PATH/OLD_FILE_NAME.EXT> <NEW/FILE/PATH/NEW_FILE_NAME.EXT>`
<br>
copy a directory: 		`cp -r <OLD/DIRECTORY/PATH/> <NEW/DIRECTORY/PATH>`
<br>
make directory: 	`mkdir <DIRECTORY_NAME>`
<br>
update file: 		`touch <FILE_NAME>`
<br>
<br>
# navigating:
go back 1 folder in a directory: 	`cd ..`
<br>
go back multiple folders: 		`cd ../../..`
<br>
reference current directory: 		`./`
<br>
reference home folder: 			`~/`
<br>
see current file path: 			`pwd`
<br>
to quit/kill a jupyter notebook: 	`ctrl+c+c`
<br>
<br>
# searching:

## viewing files and subdirectories within a directory
list all contents of a directory: 			`ls`
<br> 
list directory contents, including hidden files: 	`ls -a`
<br>
look for files with a specific file extension: 		`ls *.<EXTENSION>`
files that start with a specific phrase: 		`ls <xx>*`
<br>
files that contain a specific phrase: 			`ls *<xx>*`
<br>
can compound multiple searches:				`ls <xx>*<xx>*.<EXTENSION>`

## searching for patterns within files/directories: 
```
grep [OPTIONS] "<PATTERN_TO_MATCH>" <FILE/DIRECTORIES_TO_SEARCH_IN>
```
| Option | Meaning |
|:------:|:--------|
| -c | print only a count of the # of lines that match pattern |
| -l | list filenames only |
| -h | display matched lines but not filenames |
| -n | list matched lines and their line numbers |
| -v | list lines that *do not* match the pattern |
| -i | ignore case when matching |
| -w | match the whole word |
| -A n | print searched line and nlines *after* the result |
| -B n | print searched line and nlines *before* the result |
| -C n | print searched line and nlines before and after the result |

Examples:
<br>
display filenames that contain a given string/pattern: `grep -l "<PATTERN_TO_MATCH>" *`
<br>
get line numbers that contain a given string in a specific file: `grep -n "<PATTERN_TO_MATCH>" <FILE_NAME>`
<br>
search for a string, ignoring case, across all files of a certain type: `grep -i -n <PATTERN_TO_MATCH> *.<EXT>`
<br>
<br>
# Copy file from a server onto desktop:
1. Open terminal and navigate to the folder on my local desktop that I want to copy to
2. use command ‘scp’ with the file path on the server followed by the local file path
``` 
> cd ~/file/path/to/copy/into
> scp dmkumar@discover.nccs.nasa.gov:/file/path/to/copy/from ./
```
3. Follow prompts to enter log-in tokens/passwords/etc. for remote server

<br>

To copy all files with a certain extension within a directory, need to use single quotation marks around path:
```
scp dmkumar@discover.nccs.nasa.gov:'/file/path/to/copy/from/*.<EXT>' ./
```

<br>

To copy an entire directory, need to specify recursive copy:
```
scp -r dmkumar@discover.nccs.nasa.gov:'/file/path/to/copy/from/' ./
```
<br>
<br>
# Misc. Info
to quit/kill current command: 		`ctrl+c`
<br>
move cursor to start of line: 		`ctrl+a`
<br>
move cursor to end of line: 		`ctrl+e`
<br>
delete from cursor to end of line: 	`ctrl+k`
<br>
delete from cursor to start of line: 	`ctrl+u`
<br>
absolute path - universal
<br>
relative path - points at a path based on current directory
<br>
<br>
# Vim editor
*(This editor opens files in read-only mode)*
<br>
to edit the file, type: 				`i`
<br>
to exit edit mode: 					`esc`
<br>
save & quit: 						`:wq`
<br>
quit without saving (no changes made): 					`:q`
<br>
quit without saving + override: 			`:q!`
<br>
search for a pattern: 					`:%s/<string>`
<br>
replace instances of a pattern on current line: 	`:s/<string>/<replacement>/g`
<br>
replace all instances of a pattern: 			`:%s/<string>/<replacement>/g`
<br>
delete all instances of a pattern: 			`:%s/<string>//g`
<br>
delete all instances of a pattern with confirmation: 	`:%s/<string>//gc`
<br>
<br>
<br>
# emacs editor
save: `ctrl+x+s`
<br>
exit: `ctrl+x+c`









