

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Does an incremental search as in modern browsers
set incsearch
" Highlight the search term
set hlsearch
" Show matching brackets when text indicator is over them
set showmatch
" Set Visual Bell instead of a sound bell
" set vb
" No annoying sound on errors
set noerrorbells
set vb
set t_vb=
set tm=500
" Start from the same indent as of previous line 
set smartindent
" Does an incremental search as in modern browsers
set smartcase

" Ignore compiled files
set wildignore=*.o,*~,*.pyc

" Set tab character to 4 spaces 
set expandtab
set tabstop=4
set shiftwidth=4
""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""

set laststatus=2
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \ Line:\ %l
" set statusline=
" set statusline+=%4*\ %04l/%03c\ 
syntax on
syntax sync fromstart

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Helper functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Returns true if paste mode is enabled
function! HasPaste()
    if &paste
        return 'PASTE MODE  '
    en
    return ''
endfunction


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set t_Co=256
colorscheme molokai
" set background=dark

set foldmethod=indent
