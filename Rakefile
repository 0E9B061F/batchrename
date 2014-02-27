file "ui_batchrename.py" => "batchrename.ui" do
	sh "pyuic4 batchrename.ui -o ui_batchrename.py"
end

task :zip do
	if File.exist?("batchrename.zip")
		sh "rm batchrename.zip"
	end
	sh "git archive --format=zip --prefix=batchrename/ --output=batchrename.zip HEAD"
end

task :ico do
	sh "png2ico icon.ico icon64.png icon32.png icon16.png"
end

task :default => "ui_batchrename.py"

