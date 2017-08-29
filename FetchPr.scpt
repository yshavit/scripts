# Run as osascript FetchPr.scpt <pr-num>
# Use google chrome to fetch the PR. Assumes you're already logged in, and the PR is valid.
on run argv
	set pr_num to item 1 of argv
	tell application "Google Chrome"
		set active_window to window 1
		set active_tab to active tab index of active_window
		set pr_url to "https://github.com/sqrrldata/sqrrl/pull/" & pr_num & ".diff"
		log "opening " & pr_url & "..."
		open location pr_url
		set opened_tab to active tab index of active_window
		repeat while (loading of tab active_tab of active_window)
		end repeat
		delay 5
		log "opening as view-source" & "..."
		set outfile to "/tmp/pr-" & pr_num & ".diff"
		save active tab of active_window in outfile as "only html"
		delay 5
		log "saved " & outfile
		close active tab of active_window
		close tab opened_tab of active_window
		set active tab index of active_window to active_tab
	end tell
  return outfile
end run
