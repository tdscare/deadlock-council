cd /tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad
f=council/apply/chunk1/out/$1.js
node a3/walk1.js $f | tail -${2:-60}; node a12/check.js $f
