import React, { useContext } from 'react';
import { ProductContext, SessionContext, ChatContext } from '../../../../contexts';
import { useTranslation } from 'react-i18next';

import './Badges.css';

import { Button as NeButton, Badge as NeBadge } from '@nintexglobal/earthling-react';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import { styled } from '@mui/material/styles';

const LightTooltip = styled(({ className, ...props }) => (
	<Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
	[`& .${tooltipClasses.tooltip}`]: {
		backgroundColor: theme.palette.common.white,
		color: 'rgba(0, 0, 0, 0.87)',
		boxShadow: theme.shadows[1],
		fontSize: 12,
		font: 'Montserrat',
	},
}));

const Badges = () => {
	const { t } = useTranslation();
	const { productId } = useContext(ProductContext);
	const { expireCookie, SESSION_ID_COOKIE } = useContext(SessionContext);
	const { responseMode, setResponseMode } = useContext(ChatContext);
	
	const handleNew = () => {
		expireCookie(SESSION_ID_COOKIE);
		window.location.reload();
	};

	const handleSummarize = () => {
		if (!responseMode) {
			setResponseMode('summarized');
		} else if (responseMode !== 'sent') {
			setResponseMode();
		}
	};

	return (
		<div className="top-right-tags">
			{!productId ? (<>
				{/* <ChangeProduct /> */}
				<NeButton leftIconType='refresh' onNeClick={handleNew} variant={
					responseMode === 'sent' ? 'destructive' : 'primary'
				}>
                    Trigger Expire
				</NeButton>
				
				<NeButton rightIconType='search' onNeClick={handleSummarize} variant={
					responseMode ? 'primary' : 'secondary'
				}>
                    Summarized Response
				</NeButton>
			</>) : (<>
				<NeBadge variant='default' container='outline' label={t('chatBot.badge.experimental')} />

				<LightTooltip 
					title={t('chatBot.badge.betaTooltip')}
					slotProps={{popper: {modifiers: [{
						name: 'offset',
						options: {
							offset: [-170, -14],
						}
					}]}}}
				>
					<NeBadge variant='error' container='filled' label='BETA'/>
				</LightTooltip >
			</>)}
		</div>
	);
};

export default Badges;