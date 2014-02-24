file "ui_batchrename.py" => "batchrename.ui" do
  sh "pyuic4 batchrename.ui -o ui_batchrename.py"
end

task :zip do
	if File.exist?("batchrename.zip")
		sh "rm batchrename.zip"
	end
	sh "git archive --format=zip --prefix batchrename/ HEAD > batchrename.zip"
end

task :py2exe do
	sh "python setup.py py2exe --includes sip"
end

task :default => "ui_batchrename.py"

