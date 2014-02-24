file "ui_batchrename.py" => "batchrename.ui" do
  sh "pyuic4 batchrename.ui -o ui_batchrename.py"
end

task :zip do
	sh "git archive --format=zip --prefix batchrename/ HEAD > batchrename.zip"
end

task :default => "ui_batchrename.py"

