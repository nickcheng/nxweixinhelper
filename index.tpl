% import os

% if params['csv']:
<ul>
	<li>Downloads
    <ul>
% for f in params['csv']:
      <li><a href='/download?fn={{os.path.split(f)[1]}}'>{{os.path.split(f)[1]}}</a></li>
% end
    </ul>
	</li>
</ul>
% end
