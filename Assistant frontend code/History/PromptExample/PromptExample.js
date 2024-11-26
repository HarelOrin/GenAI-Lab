import React, { useContext } from 'react';
import { ChatContext, ProductContext } from '../../../../contexts';
import { useTranslation } from 'react-i18next';

import './PromptExample.css';

const PromptExample = () => {
	const { t } = useTranslation();
	const { setMessages, sendMessage } = useContext(ChatContext);
	const { product } = useContext(ProductContext);

	const handleClick = (e) => {
		setMessages((prevMessages) => [
			...prevMessages,
			{
				id: 0,
				role: 'user',
				content: e.target.innerHTML,
				sources: null,
			},
		]);

		sendMessage(e.target.innerHTML, product.id);
	};

	return (
		<div className="examples">
			<div className="option" onClick={handleClick}>
				{t('promptExamples.option1')}
			</div>
			<div className="option" onClick={handleClick}>
				{t('promptExamples.option2')}
			</div>
			<div className="option" onClick={handleClick}>
				{t('promptExamples.option3')}
			</div>
		</div>
	);
};

export default PromptExample;