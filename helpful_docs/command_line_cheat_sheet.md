# files:
remove a file: 		`rm <filename>`
<br>
remove a folder: 	`rm -r <folder>`
<br>
rename a file: 		`mv <oldfilename> <newfilename>`
<br>
copy a file: 		`cp <oldfilepath/*> <newfilepath>`
<br>
make directory: 	`mkdir <directoryname>`
<br>
update file: 		`touch <filename>`


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


# searching:
list all contents of a directory: 			`ls`
<br> 
list directory contents, including hidden files: 	`ls -a`
<br>
look for files with a specific file extension: 		`ls *.<extension>`
files that start with a specific phrase: 		`ls <xx>*`
<br>
files that contain a specific phrase: 			`ls *<xx>*`
<br>
can compound multiple searches:				`ls <xx>*<xx>*.<extension>`


# Copy file from a server onto desktop:
1. Open terminal and navigate to the folder on my local desktop that I want to copy to
2. use command ‘scp’ with the file path on the server followed by the local file path
``` 
> cd ~/file/path/to/copy/into
> scp dmkumar@discover.nccs.nasa.gov:/file/path/to/copy/from ./
```
3. Follow prompts to enter log-in tokens/passwords/etc. for remote server


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

# emacs editor
save: `ctrl+x+s`
<br>
exit: `ctrl+x+c`









