import React, { useContext } from 'react';
import { ProductContext } from '../../contexts';
import { useTranslation } from 'react-i18next';

// import ChangeProduct from './ChangeProduct.js';
import History from './History/History.js';
import Query from './Query/Query.js';
import BackgroundImg from './BackgroundImg.js';

import './ChatBot.css';

import { Button as NeButton } from '@nintexglobal/earthling-react';


const ChatBot = () => {
	const { t } = useTranslation();
	const { productId, searchQuery } = useContext(ProductContext);

	return (
		<div className="chatbot-container">
			{/* Render background images conditionally on screen width */}
			<div className="backgroundImg">
				<BackgroundImg />
			</div>

			{/* Back button to search results */}
			{searchQuery && productId && (
				<div className="back-btn">
					<NeButton
						leftIconType='caretLeft'
						variant='secondary'
						onNeClick={() => window.top.location.href = `https://help.nintex.com/en-US/docgensf/Results.htm?q=${searchQuery}`}
					>
						{t('chatBot.backButton')}
					</NeButton>
				</div>
			)}

			<div className="content-container">
				<History className="history" />

				<Query className="query" />
			</div>
		</div>
	);
};

export default ChatBot;
