import React, { useContext } from 'react';
import { ProductContext } from '../../../../contexts';
import { useTranslation } from 'react-i18next';
import packageJson from '../../../../../package.json';

import './Footer.css';

const Footer = () => {
	const { t } = useTranslation();
	const { productId } = useContext(ProductContext);
	const versionNumber = packageJson.version;

	return (
		<div className='footer-wrapper'>
			<p className="footer-p right-align">
				<a href={t('footer.links.termsOfUse')} className="link">{t('footer.linkDisplay.termsOfUse')}</a>
				<a href={t('footer.links.privacyPolicy')} className="link">{t('footer.linkDisplay.privacyPolicy')}</a>
				<a href={t('footer.links.security')} className="link">{t('footer.linkDisplay.security')}</a>
				<a href={t('footer.links.legal')} className="link no-border">{t('footer.linkDisplay.legal')}</a>
			</p>
			{!productId && 
				<p className="footer-p left-align">
					version: {versionNumber}
				</p>
			}
		</div>
	);
};

export default Footer;
