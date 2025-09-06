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
<br>
move cursor to start of line: 		`ctrl+a`
<br>
move cursor to end of line: 		`ctrl+e`
<br>
delete from cursor to end of line: 	`ctrl+k`
<br>
delete from cursor to start of line: 	`ctrl+u`
<br>
to quit/kill current command: 		`ctrl+c`
<br>
to quit/kill a jupyter notebook: 	`ctrl+c+c`
<br>
<br>
<br>

# operating on files and directories:
create or update a file: 		`touch <FILE_NAME>`
<br>
(if the file does not already exist, this command will create the file. If it does exist, it will refresh the file)
<br>

rename a file: 		`mv <OLD_FILE_NAME> <NEW_FILE_NAME>`
<br>

copy a file: 		`cp <OLD/FILE/PATH/OLD_FILE_NAME.EXT> <NEW/FILE/PATH/NEW_FILE_NAME.EXT>`
<br>

move a file to different directory:        `mv <OLD/FILE/PATH/OLD_FILE_NAME.EXT> <NEW/FILE/PATH/>`
<br>

remove a file: 		`rm <FILE_NAME>`
<br>
(this will result in a prompt asking to confirm you want to delete)

remove a file without prompt:       `rm -f <FILE_NAME>`
<br>
<br>

make a new directory: 	`mkdir <DIRECTORY_NAME>`
<br>

copy a directory: 		`cp -r <OLD/DIRECTORY/PATH/> <NEW/DIRECTORY/PATH>`
<br>

copy a directory, preserve symlinks:  `rsync -av </OLD/DIRECTORY/PATH/> </NEW/DIRECTORY/PATH/>`
<br>

copy a directory, dereference symlinks and get real files: `rsync -avL </OLD/DIRECTORY/PATH/> </NEW/DIRECTORY/PATH/>`
<br>
(this will give you a real copy of the file in the destination)
<br>

copy a directory, ignore symlinks: `rsync -av --no-links </OLD/DIRECTORY/PATH/> </NEW/DIRECTORY/PATH/>`
<br>

move a directory:       `mv -r <OLD/DIRECTORY/PATH/> <NEW/DIRECTORY/PATH>`
<br>

remove a directory and contents: 	`rm -r <DIRECTORY_NAME>` 
<br>
(this will generate a prompt asking you to confirm delete for everything within the directory)

remove a directory and contents without prompt:     `rm -rf <DIRECTORY_NAME>`
<br>
<br>

create a symbolic link: `ln -s /path/to/file /path/to/symlink`
<br>

edit a symbolic link: `ln -sf /path/to/file /path/to/symlink`
<br>
(note that an *absolute path* is universal while a *relative path* points at a path based on the current directory. This distinction is particularly important to remember when using symlinks)
<br>
<br>

### Moving files between a secure server and your local drive:
use command 'scp' with the file path on the server followed by the local file path. After issuing the command below, follow the prompts to enter log-in tokens/passwords/etc. necessary to access the secure server
``` 
> scp username@server.account.ext:/file/path/to/copy/from/<filename> /file/path/to/copy/into/<optional_new_filename>
```

To copy all files with a certain extension within a directory, need to use single quotation marks around path:
```
> scp username@server.account.ext:'/file/path/to/copy/from/*.<EXT>' /file/path/to/copy/into
```

To copy an entire directory, need to specify recursive copy:
```
> scp -r username@server.account.ext:'/file/path/to/copy/from/' /file/path/to/copy/into
```
<br>
<br>
<br>

# searching:
## viewing files and subdirectories within your current directory:
print names and metadata of all content: 	`l`
<br> 
list names and metadata of all content, human-readable format: 	`l -h`
<br> 
list names only: 	`ls`
<br> 
list directory contents, including hidden files: 	`ls -a`
<br>
list only files with a specific file extension: 	`ls *.<EXTENSION>`
<br>
list only files that start with a specific phrase: 		`ls <xx>*`
<br>
list only files that contain a specific phrase: 	`ls *<xx>*`
<br>
compound multiple search queries:		`ls <xx>*<xx>*.<EXTENSION>`
<br>
list directory contents, names and sizes in human readable format:      `ls -lh`
<br>
list directory contents, names and sizes in sorted in descending order:     `ls -lhS`
<br>
list directory contents, names and sizes in sorted in ascending order:     `ls -Srlh`
<br>
list subdirectory paths and size of all contents within each subdirectory:  `du -h`
<br>
<br>

## searching for patterns in file and directory names:
```
find <PATH/TO/DATA/> [OPTIONS] "<PATTERN_TO_MATCH>"
```
| Option | Meaning | Example |
|:------:|:--------|:--------|
| -type | search only for files (f) or directories (d) | `find ./ -type f` |
| -name | strings or extensions to match | `find ./ -name "*.nc"` |
| -not -name | find all files/dirs that DO NOT match strings/extensions | `find ./ -not -name "*.nc"` |
| -or | combine searches | `find ./ -name "*.nc" -or -name "*.txt"` |
| -maxdepth | set max number of levels to descend | `find ./ -maxdepth 2 -name "*.nc"` |

The default response of a find function is to print the matching values, but, you can perform other operations on the results:
| Option | Meaning | Example |
|:------:|:--------|:--------|
| -delete | permanently remove matching files/dirs | `find ./ -type f -name "*~" -delete` |
| -exec | perform unlimited operations on matching files/dirs | `find ./ -name "*.nc" -exec mv {} <NEW/PATH/> \;` |

**You can also combine the find function to customize what is printed:**
<br>
to list the matching files in sorted order:        `find <PATH/TO/DATA/> -type f -name "*.nc" | sort -V`
<br>
sort the matching files but show only the last 3:  `find <PATH/TO/DATA/> -type f -name "*.nc" | sort -V | tail -3`
<br>

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

**Examples:**
<br>
display filenames that contain a given string/pattern: `grep -l "<PATTERN_TO_MATCH>" *`
<br>
get line numbers that contain a given string in a specific file: `grep -n "<PATTERN_TO_MATCH>" <FILE_NAME>`
<br>
search for a string, ignoring case, across all files of a certain type: `grep -i -n "<PATTERN_TO_MATCH>" *.<EXT>`
<br>
<br>
<br>

# File Editors
## Vim
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
jump to bottom of file:             `esc + shift + g`
<br>
jump to top of file:                `gg`
<br>
delete everything from cursor position to start of line: 			`ctrl+u`
<br>
delete a block of text:    `v V (then scroll down to the start of the last line you want to delete) d`
<br> 

**Modify default settings**
```
# create a .vimrc file in your home directory
touch ~/.vimrc

# set tabstop and shiftwidth preferences
echo "set tabstop=4 shiftwidth=4" >> ~/.vimrc
```
<br>
<br>

## emacs
save: `ctrl+x+s`
<br>
exit: `ctrl+x+c`
<br>
<br>
<br>

# storage limits:
most hpc systems implement storage quotas. They should have their own documentation for how to check storage quotas, but here are some examples.
<br>
list project directories and storage quotas on Discover: `showquota -h`
(-h option prints results in human-readable format)
<br>
list project directories and storage quotas on NCAR system: `gladequota -h`
