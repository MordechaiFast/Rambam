/**
 * Calendar Units: Year, Month, Day
 * 
 * Implements the Hebrew calendar system from Maimonides (Rambam).
 * Based on a lunar month of 29d 12h 793 parts, with a 19-year cycle.
 */

import { TimeInterval, TimeInWeek } from './timeMeasures';

// ==================== Constants ====================

const CHALAKIM_IN_HOUR = 1080;
const LUNAR_MONTH = new TimeInterval(29, 12, 793, CHALAKIM_IN_HOUR);
const LUNAR_YEAR = LUNAR_MONTH.multiply(12);
const LEAP_YEAR = LUNAR_MONTH.multiply(13);
const LUNAR_MONTH_REMAINDER = new TimeInWeek(...LUNAR_MONTH.toArray());
const LUNAR_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER.multiply(12) as TimeInWeek;
const LEAP_YEAR_REMAINDER = LUNAR_MONTH_REMAINDER.multiply(13) as TimeInWeek;

const BHRD = new TimeInWeek(6, 14).subtract(LUNAR_YEAR_REMAINDER) as TimeInWeek;

const CYCLE_YEARS = 19;
const CYCLE = LUNAR_YEAR.multiply(12).add(LEAP_YEAR.multiply(7)) as TimeInterval;
const CYCLE_REMAINDER = LUNAR_YEAR_REMAINDER.multiply(12)
  .add(LEAP_YEAR_REMAINDER.multiply(7)) as TimeInWeek;

const LEAP_YEARS = new Set([0, 3, 6, 8, 11, 14, 17, 19]);
const ADU = new Set([1, 4, 6]); // Days that Rosh Hashana cannot fall on
const GTRD = new TimeInWeek(7, 18).subtract(LUNAR_YEAR_REMAINDER) as TimeInWeek;
const BTU_TKPT = new TimeInWeek(3, 18).add(LEAP_YEAR_REMAINDER) as TimeInWeek;

const MONTH_NAMES = [
  'Tishrei', 'Marchesvan', 'Kislev', 'Teves', 'Shevat', 'Addar',
  'Nissan', 'Iyyar', 'Sivan', 'Tamuz', 'Av', 'Elul'
];

const MONTH_NAMES_IN_LEAP_YEAR = [
  'Tishrei', 'Marchesvan', 'Kislev', 'Teves', 'Shevat', 'Addar I', 'Addar II',
  'Nissan', 'Iyyar', 'Sivan', 'Tamuz', 'Av', 'Elul'
];

const SHORT_MONTH = 29;
const WHOLE_MONTH = 30;

// ==================== Year ====================

export class Year {
  years_from_creation: number;
  cycles_to_year: number;
  place_in_cycle: number;
  molad: TimeInWeek;

  private _rosh_hashana: number | null = null;
  private _date: number | null = null;
  private _whole_months: boolean[] | null = null;
  private _year_after: Year | null = null;

  /**
   * Create a Year instance
   * @param count - The year count (relative to start_year)
   * @param start_year - Base year (default 1 = year of BHRD)
   */
  constructor(count: number, start_year: number = 1) {
    // Calculate years from creation
    this.years_from_creation = start_year - 1 + count;

    // Divide into cycles
    this.cycles_to_year = Math.floor(this.years_from_creation / CYCLE_YEARS);
    this.place_in_cycle = this.years_from_creation % CYCLE_YEARS;

    // Correct for 0 in mod 19
    if (this.place_in_cycle === 0) {
      this.cycles_to_year--;
      this.place_in_cycle = CYCLE_YEARS;
    }

    // Calculate molad of beginning of year
    this.molad = CYCLE_REMAINDER.multiply(this.cycles_to_year)
      .add(BHRD) as TimeInWeek;

    // Add remainder for years before this one in the cycle
    for (let y = 1; y < this.place_in_cycle; y++) {
      if (LEAP_YEARS.has(y)) {
        this.molad = this.molad.add(LEAP_YEAR_REMAINDER) as TimeInWeek;
      } else {
        this.molad = this.molad.add(LUNAR_YEAR_REMAINDER) as TimeInWeek;
      }
    }
  }

  toString(): string {
    return String(this.years_from_creation);
  }

  /**
   * Get the day of week of Rosh Hashana (1-7, where 7 is Shabbat)
   */
  get Rosh_Hashana(): number {
    if (this._rosh_hashana !== null) return this._rosh_hashana;

    let day = this.molad.days;

    // 7:1 - Never on days 1, 4, or 6
    if (ADU.has(day)) {
      day = day + 1;
    }
    // 7:2 - If after noon, push to next day (unless it's 1, 4, or 6)
    else if (this.molad.hours >= 18) {
      if (!ADU.has((day % 7) + 1)) {
        day = day + 1;
      }
      // 7:3 - If after noon and next day is 1, 4, or 6, push two days
      else {
        day = (day % 7) + 2;
      }
    }
    // 7:4 - GTRD rule
    else if (
      day === 3 &&
      this.molad.greaterThanOrEqual(GTRD) &&
      !LEAP_YEARS.has(this.place_in_cycle)
    ) {
      day = day + 2;
    }
    // 7:5 - BTU TKPT rule
    else if (
      day === 2 &&
      this.molad.greaterThanOrEqual(BTU_TKPT) &&
      LEAP_YEARS.has(this.place_in_cycle - 1)
    ) {
      day = day + 1;
    }

    this._rosh_hashana = day;
    return day;
  }

  /**
   * Get the date of Rosh Hashana in days from Shabbos before BHRD
   */
  get date(): number {
    if (this._date !== null) return this._date;

    const objective_molad = CYCLE.multiply(this.cycles_to_year).add(BHRD) as TimeInterval;

    let accumulated = objective_molad.days;
    for (let y = 1; y < this.place_in_cycle; y++) {
      if (LEAP_YEARS.has(y)) {
        accumulated += LEAP_YEAR.days;
      } else {
        accumulated += LUNAR_YEAR.days;
      }
    }

    const result = accumulated + this.Rosh_Hashana - (this.molad.days % 7);
    this._date = result;
    return result;
  }

  /**
   * Get array indicating which months are whole (30 days)
   */
  get whole_months(): boolean[] {
    if (this._whole_months !== null) return this._whole_months;

    let months: boolean[] = [true, false, true, false, true, false,
                              true, false, true, false, true, false];

    // In leap year, insert extra Addar I as whole month
    if (LEAP_YEARS.has(this.place_in_cycle)) {
      months.splice(5, 0, true);
    }

    // Determine year type based on days between this year's RH and next year's RH
    const next_year = this.year_after;
    const days_between = (next_year.Rosh_Hashana - this.Rosh_Hashana - 1) % 7;

    let year_type: string;
    if (LEAP_YEARS.has(this.place_in_cycle)) {
      year_type = { 4: 'lacking', 5: 'orderly', 6: 'full' }[days_between] || 'orderly';
    } else {
      year_type = { 2: 'lacking', 3: 'orderly', 4: 'full' }[days_between] || 'orderly';
    }

    // Adjust Marchesvan/Kislev based on year type
    if (year_type === 'lacking') {
      months[2] = false; // Kislev becomes lacking
    } else if (year_type === 'full') {
      months[1] = true; // Marchesvan becomes whole
    }

    this._whole_months = months;
    return months;
  }

  /**
   * Get the next year
   */
  get year_after(): Year {
    if (this._year_after !== null) return this._year_after;
    this._year_after = new Year(this.years_from_creation + 1);
    return this._year_after;
  }

  /**
   * Iterate over all months in this year
   */
  *[Symbol.iterator](): Generator<Month> {
    const num_months = LEAP_YEARS.has(this.place_in_cycle) ? 13 : 12;
    for (let n = 0; n < num_months; n++) {
      yield new Month(this, n, true);
    }
  }
}

// ==================== Month ====================

export class Month {
  year: Year;
  month_count: number;
  molad: TimeInWeek;

  private _name: string | null = null;
  private _date: number | null = null;
  private _month_after: Month | null = null;

  /**
   * Create a Month instance
   * @param year - The Year this month belongs to
   * @param month_reference - Month number (0-11 from Tishrei, or 1-13 from Nissan)
   * @param start_from_tishrei - If true, month_reference is from Tishrei; else from Nissan
   */
  constructor(year: Year, month_reference: number, start_from_tishrei: boolean = false) {
    this.year = year;

    if (start_from_tishrei) {
      this.month_count = month_reference;
    } else {
      // Convert from Nissan-based to Tishrei-based
      if (month_reference > 6) {
        this.month_count = month_reference - 7;
      } else if (LEAP_YEARS.has(year.place_in_cycle)) {
        this.month_count = month_reference + 6;
      } else {
        this.month_count = month_reference + 5;
      }
    }

    // Calculate molad of this month
    this.molad = year.molad.add(
      LUNAR_MONTH_REMAINDER.multiply(this.month_count)
    ) as TimeInWeek;
  }

  toString(): string {
    return `${this.name} ${this.year}`;
  }

  /**
   * Get the name of this month
   */
  get name(): string {
    if (this._name !== null) return this._name;

    const names = LEAP_YEARS.has(this.year.place_in_cycle)
      ? MONTH_NAMES_IN_LEAP_YEAR
      : MONTH_NAMES;

    this._name = names[this.month_count];
    return this._name;
  }

  /**
   * Whether this month has 30 days
   */
  get is_whole(): boolean {
    return this.year.whole_months[this.month_count];
  }

  /**
   * Whether Rosh Chodesh is two days
   */
  get two_day_Rosh_Chodesh(): boolean {
    return this.year.whole_months[this.month_count - 1];
  }

  /**
   * Get the date of Rosh Chodesh (in days from reference)
   */
  get date(): number {
    if (this._date !== null) return this._date;

    let result = this.year.date;
    for (let i = 0; i < this.month_count; i++) {
      result += this.year.whole_months[i] ? WHOLE_MONTH : SHORT_MONTH;
    }

    this._date = result;
    return result;
  }

  /**
   * Get the next month
   */
  get month_after(): Month {
    if (this._month_after !== null) return this._month_after;

    if (
      this.month_count < 11 ||
      (LEAP_YEARS.has(this.year.place_in_cycle) && this.month_count === 11)
    ) {
      this._month_after = new Month(this.year, this.month_count + 1, true);
    } else {
      this._month_after = new Month(this.year.year_after, 0, true);
    }

    return this._month_after;
  }

  /**
   * Iterate over all days in this month
   */
  *[Symbol.iterator](): Generator<Day> {
    const num_days = this.is_whole ? WHOLE_MONTH : SHORT_MONTH;
    for (let d = 1; d <= num_days; d++) {
      yield new Day(this, d);
    }
  }
}

// ==================== Day ====================

export class Day {
  month: Month;
  day: number;

  private _date: number | null = null;
  private _day_of_week: number | null = null;

  /**
   * Create a Day instance
   * Automatically fixes dates past the end of the month by rolling to next month
   * @param month - The Month this day belongs to
   * @param day - Day of month (1-based)
   */
  constructor(month: Month, day: number = 1) {
    this.month = month;
    this.day = day;

    // Auto-adjust if day exceeds month length
    while (this.day > (this.month.is_whole ? WHOLE_MONTH : SHORT_MONTH)) {
      this.day -= this.month.is_whole ? WHOLE_MONTH : SHORT_MONTH;
      this.month = this.month.month_after;
    }
  }

  toString(): string {
    return `${this.day} ${this.month}`;
  }

  /**
   * Add days to this day, returning a new Day
   */
  add(addend: number): Day {
    return new Day(this.month, this.day + addend);
  }

  /**
   * Get the absolute date (days from reference point)
   */
  get date(): number {
    if (this._date !== null) return this._date;
    this._date = this.month.date + this.day - 1;
    return this._date;
  }

  /**
   * Get day of week (1-7, where 7 is Shabbat)
   */
  get day_of_week(): number {
    if (this._day_of_week !== null) return this._day_of_week;

    const dayNum = this.date % 7;
    this._day_of_week = dayNum === 0 ? 7 : dayNum;
    return this._day_of_week;
  }

  /**
   * Create a Day from an absolute date number
   */
  static fromDate(dateNum: number): Day {
    let d = new TimeInterval(dateNum, 0, 0, CHALAKIM_IN_HOUR);
    let year_count = 1;
    let month_count = 0;

    // Find which year
    while (d.greaterThan(CYCLE)) {
      year_count += CYCLE_YEARS;
      d = d.subtract(CYCLE) as TimeInterval;
    }

    for (let y = 1; y <= CYCLE_YEARS; y++) {
      const year_length = LEAP_YEARS.has(y) ? LEAP_YEAR : LUNAR_YEAR;
      if (d.greaterThan(year_length)) {
        year_count++;
        d = d.subtract(year_length) as TimeInterval;
      } else {
        break;
      }
    }

    // Find which month
    while (d.greaterThan(LUNAR_MONTH)) {
      month_count++;
      d = d.subtract(LUNAR_MONTH) as TimeInterval;
    }

    const month = new Month(new Year(year_count), month_count, true);
    let day = dateNum - month.date + 1;

    if (day < 1) {
      const prev_month = month_count > 0
        ? new Month(new Year(year_count), month_count - 1, true)
        : new Month(new Year(year_count - 1), 6, true);
      day = dateNum - prev_month.date + 1;
      return new Day(prev_month, day);
    }

    return new Day(month, day);
  }
}
