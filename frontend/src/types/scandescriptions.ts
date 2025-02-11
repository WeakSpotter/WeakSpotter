export enum ScanDescriptionCategory {
    content = 0, 
    host = 1,
    code = 2,
    privacy = 3,
    other = 4,
}

export interface ScanDescription {
    id: number;
    scanid: number;
    category: ScanDescriptionCategory;
    longdescription: string;
    shortdescription: string;
}

export const getScanDescriptionCategoryText = (category: ScanDescriptionCategory): string => {
    switch (category) {
        case ScanDescriptionCategory.content:
            return "Content";
        case ScanDescriptionCategory.host:
            return "Host";
        case ScanDescriptionCategory.code:
            return "Code";
        case ScanDescriptionCategory.privacy:
            return "Privacy";
        case ScanDescriptionCategory.other:
            return "Other";
        default:
            return "Unknown";
    }
}