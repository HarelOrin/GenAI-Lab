import React from 'react';

import topLeft from '../../assets/background/topLeft.svg';
import bottomLeft from '../../assets/background/bottomLeft.svg';
import right from '../../assets/background/right.svg';

const BackgroundImg = () => {
	return (
		<div>
			<img
				src={topLeft}
				style={{ width: '112px',
					position: 'fixed',
					top: '17vh',
					left: '85px',
					zIndex: '-999',
				}}
			/>
			<img
				src={bottomLeft}
				style={{ width: '389px',
					position: 'fixed',
					top : '48vh',
					left: '-96px',
					zIndex: '-999',
				}}
			/>
			<img
				src={right}
				style={{ width: '445px',
					position: 'fixed',
					top : '17vh',
					right: '-153px',
					zIndex: '-999',
				}}
			/>
		</div>
	);
};

export default BackgroundImg;